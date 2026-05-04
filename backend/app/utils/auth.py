import os
import time
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import defaultdict

import bcrypt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = int(os.getenv("TOKEN_EXPIRE_HOURS", "24"))
ACCESS_PASSWORD = os.getenv("ACCESS_PASSWORD", "")
JWT_SECRET = os.getenv("JWT_SECRET", "") or secrets.token_hex(32)

security = HTTPBearer(auto_error=False)

_login_attempts: dict[str, list[float]] = defaultdict(list)
MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 300


def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    pwd_bytes = plain.encode("utf-8")[:72]
    hash_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hash_bytes)


_stored_hash: Optional[str] = None


def get_password_hash() -> str:
    global _stored_hash
    if _stored_hash is None:
        if not ACCESS_PASSWORD:
            _stored_hash = ""
        else:
            _stored_hash = hash_password(ACCESS_PASSWORD)
    return _stored_hash


def check_rate_limit(client_ip: str) -> None:
    now = time.time()
    attempts = _login_attempts[client_ip]
    _login_attempts[client_ip] = [t for t in attempts if now - t < LOCKOUT_SECONDS]
    if len(_login_attempts[client_ip]) >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="登录尝试过于频繁，请5分钟后重试",
        )


def record_login_attempt(client_ip: str) -> None:
    _login_attempts[client_ip].append(time.time())


def clear_login_attempts(client_ip: str) -> None:
    _login_attempts.pop(client_ip, None)


def create_access_token(expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=TOKEN_EXPIRE_HOURS))
    payload = {"exp": expire, "iat": datetime.now(timezone.utc)}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证已过期，请重新登录",
        )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    if not ACCESS_PASSWORD:
        return {"authenticated": True}
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证凭据",
        )
    verify_token(credentials.credentials)
    return {"authenticated": True}


async def optional_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[dict]:
    if not ACCESS_PASSWORD:
        return None
    if credentials is None:
        return None
    try:
        verify_token(credentials.credentials)
        return {"authenticated": True}
    except HTTPException:
        return None
