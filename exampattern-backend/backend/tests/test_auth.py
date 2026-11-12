import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security import TokenError, create_access_token, decode_access_token, hash_password, verify_password
import pytest

API = "/api/v1/auth"
CREDS = {"email": "a@example.com", "password": "correct-horse-battery"}


def test_password_hash_roundtrip():
    h = hash_password("secret-pass-1")
    assert h != "secret-pass-1" and verify_password("secret-pass-1", h) and not verify_password("nope", h)


def test_token_roundtrip_and_rejections():
    uid = uuid.uuid4()
    token, _ = create_access_token(uid)
    assert decode_access_token(token) == uid
    with pytest.raises(TokenError):
        decode_access_token("garbage")
    expired, _ = create_access_token(uid, expires_minutes=-1)
    with pytest.raises(TokenError):
        decode_access_token(expired)
    wrong_key = jwt.encode({"sub": str(uid), "exp": datetime.now(timezone.utc) + timedelta(minutes=5)}, "other-key-other-key-other-key-1234", algorithm="HS256")
    with pytest.raises(TokenError):
        decode_access_token(wrong_key)
    none_alg = jwt.encode({"sub": str(uid), "exp": datetime.now(timezone.utc) + timedelta(minutes=5)}, None, algorithm="none")
    with pytest.raises(TokenError):
        decode_access_token(none_alg)


def test_register_and_login_and_me(client):
    r = client.post(f"{API}/register", json={**CREDS, "email": "A@Example.com", "full_name": "Asha"})
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "a@example.com" and "password" not in body and "hashed_password" not in body

    r = client.post(f"{API}/login", json=CREDS)
    assert r.status_code == 200 and r.json()["token_type"] == "bearer"
    token = r.json()["access_token"]

    r = client.get(f"{API}/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200 and r.json()["email"] == "a@example.com"


def test_duplicate_email_conflict(client):
    assert client.post(f"{API}/register", json=CREDS).status_code == 201
    r = client.post(f"{API}/register", json=CREDS)
    assert r.status_code == 409 and r.json()["error"]["code"] == "conflict"


def test_weak_password_and_bad_email_rejected(client):
    r = client.post(f"{API}/register", json={"email": "b@example.com", "password": "short"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "validation_error"
    assert client.post(f"{API}/register", json={"email": "not-an-email", "password": "long-enough-pw"}).status_code == 422


def test_login_failures_are_uniform(client):
    client.post(f"{API}/register", json=CREDS)
    wrong_pw = client.post(f"{API}/login", json={**CREDS, "password": "wrong-password"})
    unknown = client.post(f"{API}/login", json={"email": "nobody@example.com", "password": "whatever-pw"})
    assert wrong_pw.status_code == unknown.status_code == 401
    assert wrong_pw.json() == unknown.json()


def test_me_requires_valid_token(client):
    assert client.get(f"{API}/me").status_code == 401
    assert client.get(f"{API}/me", headers={"Authorization": "Bearer nope"}).status_code == 401
    expired, _ = create_access_token(uuid.uuid4(), expires_minutes=-1)
    assert client.get(f"{API}/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401


def test_token_for_deleted_user_rejected(client):
    token, _ = create_access_token(uuid.uuid4())  # valid signature, no such user
    assert client.get(f"{API}/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_auth_rate_limit(client):
    limiter.enabled = True
    limiter.reset()
    codes = [client.post(f"{API}/login", json={"email": "x@example.com", "password": "bad-password"}).status_code for _ in range(12)]
    assert 429 in codes and codes[0] == 401
    limiter.enabled = False
