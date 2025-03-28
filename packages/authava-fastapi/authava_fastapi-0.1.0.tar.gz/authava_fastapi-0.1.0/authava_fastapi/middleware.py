from typing import Any, Awaitable, Callable, Optional, Union

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from .client import AuthavaClient, AuthavaUser


class AuthavaMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for Authava authentication.
    
    This middleware:
    1. Validates the session cookie
    2. Attaches the user to the request state
    3. Handles unauthorized access
    
    Example:
        ```python
        from fastapi import FastAPI
        from authava_fastapi import AuthavaMiddleware
        
        app = FastAPI()
        app.add_middleware(
            AuthavaMiddleware,
            domain="auth.yourdomain.com",
            exclude_paths=["/health", "/metrics"],
        )
        ```
    """

    def __init__(
        self,
        app: ASGIApp,
        domain: str,
        exclude_paths: Optional[list[str]] = None,
        unauthorized_handler: Optional[Callable[[Request], Response]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the middleware.
        
        Args:
            app: The FastAPI application
            domain: Your Authava domain
            exclude_paths: List of paths to exclude from authentication
            unauthorized_handler: Custom handler for unauthorized requests
            **kwargs: Additional configuration for AuthavaClient
        """
        super().__init__(app)
        self.client = AuthavaClient(domain=domain, **kwargs)
        self.exclude_paths = exclude_paths or []
        self.unauthorized_handler = unauthorized_handler or self._default_unauthorized_handler

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process the request.
        
        Args:
            request: The incoming request
            call_next: The next middleware/endpoint
            
        Returns:
            The response
        """
        # Skip authentication for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        cookie = request.headers.get("cookie")
        if not cookie:
            return await self.unauthorized_handler(request)

        session = await self.client.get_session(cookie)
        if not session:
            return await self.unauthorized_handler(request)

        # Attach user to request state
        request.state.user = session.user
        
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Clear cache on errors to prevent stale data
            self.client.clear_session_cache(cookie)
            raise

    async def _default_unauthorized_handler(self, request: Request) -> Response:
        """Default handler for unauthorized requests."""
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"},
        )


class EnsureUserExists(BaseHTTPMiddleware):
    """
    Middleware to ensure Authava users exist in your database.
    
    This middleware:
    1. Checks if the authenticated user exists in your database
    2. Creates the user if they don't exist
    3. Attaches the database user to the request state
    
    Example:
        ```python
        from fastapi import FastAPI
        from authava_fastapi import EnsureUserExists
        from sqlalchemy.ext.asyncio import AsyncSession
        
        async def get_user_service():
            # Your user service implementation
            pass
        
        app = FastAPI()
        app.add_middleware(
            EnsureUserExists,
            get_user_service=get_user_service,
        )
        ```
    """

    def __init__(
        self,
        app: ASGIApp,
        get_user_service: Callable[[], Any],
        error_handler: Optional[Callable[[Request, Exception], Response]] = None,
    ) -> None:
        """Initialize the middleware.
        
        Args:
            app: The FastAPI application
            get_user_service: Function that returns your user service
            error_handler: Custom handler for errors
        """
        super().__init__(app)
        self.get_user_service = get_user_service
        self.error_handler = error_handler or self._default_error_handler

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process the request.
        
        Args:
            request: The incoming request
            call_next: The next middleware/endpoint
            
        Returns:
            The response
        """
        auth_user = getattr(request.state, "user", None)
        if not auth_user:
            return await call_next(request)

        try:
            user_service = self.get_user_service()
            db_user = await user_service.find_or_create_user(
                auth_id=auth_user.id,
                email=auth_user.email,
                extra=auth_user.extra,
            )
            request.state.db_user = db_user
            return await call_next(request)
        except Exception as e:
            return await self.error_handler(request, e)

    async def _default_error_handler(self, request: Request, error: Exception) -> Response:
        """Default handler for errors."""
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )