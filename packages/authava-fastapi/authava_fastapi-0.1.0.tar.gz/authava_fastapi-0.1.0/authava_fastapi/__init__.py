"""FastAPI integration for Authava authentication service."""

from .client import AuthavaClient, AuthavaSession, AuthavaUser
from .middleware import AuthavaMiddleware, EnsureUserExists

__version__ = "0.1.0"
__all__ = [
    "AuthavaClient",
    "AuthavaSession",
    "AuthavaUser",
    "AuthavaMiddleware",
    "EnsureUserExists",
]