# Authava FastAPI Integration

FastAPI integration for the Authava authentication service. This package provides middleware and utilities for seamless integration with FastAPI applications.

## Features

- 🚀 Async-first design
- 🔒 Session-based authentication
- 📦 Built-in session caching
- 🔄 User synchronization
- 🎯 Type hints and Pydantic models
- 📚 Comprehensive documentation

## Installation

```bash
pip install authava-fastapi
```

## Quick Start

```python
from fastapi import FastAPI, Depends
from authava_fastapi import AuthavaClient, AuthavaUser

app = FastAPI()
authava = AuthavaClient(domain="auth.yourdomain.com")

@app.get("/protected")
async def protected_route(user: AuthavaUser = Depends(authava.require_auth)):
    return {"message": f"Hello {user.email}!"}
```

## Middleware Usage

### Basic Authentication

```python
from fastapi import FastAPI
from authava_fastapi import AuthavaMiddleware

app = FastAPI()

app.add_middleware(
    AuthavaMiddleware,
    domain="auth.yourdomain.com",
    exclude_paths=["/health", "/docs"],  # Optional: paths to exclude
)

@app.get("/protected")
async def protected_route(request: Request):
    # Access the authenticated user
    user = request.state.user
    return {"email": user.email}
```

### User Synchronization

```python
from fastapi import FastAPI
from authava_fastapi import AuthavaMiddleware, EnsureUserExists
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def find_or_create_user(self, auth_id: str, email: str, extra: dict = None):
        # Your user synchronization logic here
        pass

async def get_user_service():
    # Your service initialization logic
    pass

app = FastAPI()

# Add both middlewares
app.add_middleware(AuthavaMiddleware, domain="auth.yourdomain.com")
app.add_middleware(EnsureUserExists, get_user_service=get_user_service)

@app.get("/me")
async def get_profile(request: Request):
    # Access both Authava user and database user
    auth_user = request.state.user
    db_user = request.state.db_user
    return {
        "auth_user": auth_user,
        "db_user": db_user,
    }
```

## Configuration

### Client Configuration

```python
from authava_fastapi import AuthavaClient

client = AuthavaClient(
    domain="auth.yourdomain.com",
    resolver_domain="api.yourdomain.com",  # Optional: API domain if different
    secure=True,  # Use HTTPS (default: True)
    auto_refresh=True,  # Auto refresh session (default: True)
    refresh_buffer=5,  # Minutes before expiration to refresh (default: 5)
    cache_ttl=300,  # Session cache TTL in seconds (default: 300)
)
```

### Middleware Configuration

```python
app.add_middleware(
    AuthavaMiddleware,
    domain="auth.yourdomain.com",
    exclude_paths=["/health", "/docs"],
    unauthorized_handler=custom_unauthorized_handler,  # Optional
)

app.add_middleware(
    EnsureUserExists,
    get_user_service=get_user_service,
    error_handler=custom_error_handler,  # Optional
)
```

## Session Caching

The client includes built-in caching to reduce API calls:

```python
# Get session (uses cache if available)
session = await client.get_session(cookie)

# Clear cache for a specific session
client.clear_session_cache(cookie)
```

## User Synchronization

The `EnsureUserExists` middleware helps keep your local user database in sync with Authava:

1. **Automatic**: Users are automatically created/updated on each request
2. **Flexible**: Customize user creation/update logic via your service
3. **Safe**: Error handling prevents request failures

Example service implementation:

```python
class UserService:
    async def find_or_create_user(self, auth_id: str, email: str, extra: dict = None):
        user = await User.get_by_auth_id(auth_id)
        if not user:
            user = await User.create(
                auth_id=auth_id,
                email=email,
                name=extra.get("name"),
            )
        return user
```

## Testing

The package includes utilities for testing protected routes:

```python
from authava_fastapi.testing import mock_authava_session

@pytest.mark.asyncio
async def test_protected_route(client):
    # Mock a valid session
    with mock_authava_session(
        user_id="123",
        email="test@example.com",
    ):
        response = await client.get("/protected")
        assert response.status_code == 200
```

## Examples

See the `examples` directory for complete working examples:

- `basic_app.py`: Simple FastAPI application with authentication
- `sqlalchemy_app.py`: Full example with database integration
- `custom_auth.py`: Custom authentication logic example

## Contributing

Contributions are welcome! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

## License

MIT