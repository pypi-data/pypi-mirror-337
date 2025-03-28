from typing import Any, Dict, Optional, Union, Callable
from urllib.parse import urljoin

import httpx
from cachetools import TTLCache
from pydantic import BaseModel, Field


class AuthavaUser(BaseModel):
    """Represents an authenticated Authava user."""
    id: str
    email: str
    extra: Dict[str, Any] = Field(default_factory=dict)


class AuthavaSession(BaseModel):
    """Represents an Authava session."""
    user: AuthavaUser
    redirect_url: str


class AuthavaConfig(BaseModel):
    """Configuration for the Authava client."""
    domain: str
    resolver_domain: Optional[str] = None
    secure: bool = True
    auto_refresh: bool = True
    refresh_buffer: int = 5  # minutes
    cache_ttl: int = 300  # seconds


class AuthavaClient:
    """
    FastAPI client for Authava authentication service.
    
    Example:
        ```python
        from fastapi import FastAPI, Depends
        from authava_fastapi import AuthavaClient, AuthavaUser
        
        app = FastAPI()
        authava = AuthavaClient(domain="auth.yourdomain.com")
        
        @app.get("/protected")
        async def protected_route(user: AuthavaUser = Depends(authava.require_auth)):
            return {"message": f"Hello {user.email}!"}
        ```
    """

    def __init__(self, domain: str, **kwargs: Any) -> None:
        """Initialize the Authava client.
        
        Args:
            domain: Your Authava domain (e.g., auth.yourdomain.com)
            **kwargs: Additional configuration options
        """
        self.config = AuthavaConfig(domain=domain, **kwargs)
        self.config.resolver_domain = self.config.resolver_domain or self.config.domain
        
        self._http = httpx.AsyncClient(
            base_url=f"{'https' if self.config.secure else 'http'}://{self.config.resolver_domain}",
            timeout=10.0,
        )
        
        # Cache for session data
        self._cache = TTLCache(maxsize=1000, ttl=self.config.cache_ttl)

    async def get_session(self, cookie: Optional[str] = None) -> Optional[AuthavaSession]:
        """Get the current session from a cookie.
        
        Args:
            cookie: The session cookie string
            
        Returns:
            The session data if valid, None otherwise
        """
        if not cookie:
            return None

        # Check cache first
        cache_key = f"session_{cookie}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            response = await self._http.post(
                "/session",
                headers={
                    "Accept": "application/json",
                    "Cookie": cookie,
                    "Host": self.config.domain,
                },
            )

            if response.status_code == 401:
                return None

            if response.status_code != 200:
                raise httpx.HTTPError(f"Failed to get session: {response.status_code}")

            data = response.json()
            if not data.get("user", {}).get("id") or not data.get("user", {}).get("email"):
                return None

            session = AuthavaSession.model_validate(data)
            self._cache[cache_key] = session
            return session

        except httpx.HTTPError as e:
            # Log error but don't raise to avoid exposing internals
            print(f"Authava session error: {e}")
            return None

    def clear_session_cache(self, cookie: str) -> None:
        """Clear the cached session data for a cookie."""
        cache_key = f"session_{cookie}"
        if cache_key in self._cache:
            del self._cache[cache_key]

    def require_auth(self) -> Callable:
        """FastAPI dependency for requiring authentication.
        
        Returns:
            A dependency that returns the authenticated user
            
        Example:
            ```python
            @app.get("/protected")
            async def protected_route(user: AuthavaUser = Depends(client.require_auth())):
                return {"email": user.email}
            ```
        """
        from fastapi import HTTPException, status, Request, Depends

        async def auth_dependency(request: Request) -> AuthavaUser:
            cookie = request.headers.get("cookie")
            if not cookie:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No authentication cookie provided",
                )

            session = await self.get_session(cookie)
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired session",
                )

            return session.user

        return auth_dependency

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._http.aclose()

    async def __aenter__(self) -> "AuthavaClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()