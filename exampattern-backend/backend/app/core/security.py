import uuid
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

_hasher = PasswordHash.recommended()  # Argon2id
# Used to equalise login timing when the email is unknown.
DUMMY_HASH = _hasher.hash("not-a-real-password")


class TokenError(Exception):
    """Raised for any invalid, expired or malformed token."""


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return _hasher.verify(password, hashed)


def create_access_token(subject: uuid.UUID, expires_minutes: int | None = None) -> tuple[str, int]:
    """Return (token, expires_in_seconds)."""
    minutes = expires_minutes if expires_minutes is not None else settings.access_token_expire_minutes
    now = datetime.now(timezone.utc)
    payload = {"sub": str(subject), "iat": now, "exp": now + timedelta(minutes=minutes), "jti": uuid.uuid4().hex}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm), minutes * 60


def decode_access_token(token: str) -> uuid.UUID:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],  # pinned: never trust the token header's alg
            options={"require": ["exp", "sub"]},
        )
        return uuid.UUID(payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError) as exc:
        raise TokenError("invalid token") from exc
