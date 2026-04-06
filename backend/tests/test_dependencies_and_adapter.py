from datetime import timedelta
from unittest.mock import patch

import cloudinary.exceptions
import pytest
from fastapi import HTTPException
from jose import JWTError

from application.use_cases.auth_use_cases import AuthUseCases
from domain.entities.user import Role, User
from infrastructure.adapters.cloudinary_adapter import CloudinaryAdapter
from infrastructure.api.dependencies import get_admin_user, get_current_user, get_optional_current_user
from infrastructure.auth.jwt_handler import JWTHandler
from infrastructure.persistence.in_memory_user_repository import InMemoryUserRepository


def _auth_with_user(user: User) -> AuthUseCases:
    repo = InMemoryUserRepository()
    repo.create(user)
    return AuthUseCases(repo)


def test_get_optional_current_user_no_token_returns_none() -> None:
    auth_uc = _auth_with_user(
        User(id=1, username="user_a", hashed_password="x", role=Role.USER, is_active=True)
    )
    result = get_optional_current_user(None, JWTHandler(), auth_uc)
    assert result is None


def test_get_optional_current_user_missing_sub_returns_none() -> None:
    handler = JWTHandler()
    token = handler.create_access_token({"role": "user"})
    auth_uc = _auth_with_user(
        User(id=1, username="user_b", hashed_password="x", role=Role.USER, is_active=True)
    )
    result = get_optional_current_user(token, handler, auth_uc)
    assert result is None


def test_get_optional_current_user_invalid_token_returns_none() -> None:
    auth_uc = _auth_with_user(
        User(id=1, username="user_c", hashed_password="x", role=Role.USER, is_active=True)
    )
    with patch.object(JWTHandler, "decode_token", side_effect=JWTError("bad")):
        result = get_optional_current_user("bad-token", JWTHandler(), auth_uc)
    assert result is None


def test_get_optional_current_user_valid_token_returns_user() -> None:
    user = User(id=1, username="validuser", hashed_password="x", role=Role.USER, is_active=True)
    auth_uc = _auth_with_user(user)
    handler = JWTHandler()
    token = handler.create_access_token({"sub": "validuser"})

    result = get_optional_current_user(token, handler, auth_uc)
    assert result is not None
    assert result.username == "validuser"


def test_get_current_user_branches() -> None:
    with pytest.raises(HTTPException) as exc_unauth:
        get_current_user(None)
    assert exc_unauth.value.status_code == 401

    inactive = User(id=2, username="inactive_user", hashed_password="x", role=Role.USER, is_active=False)
    with pytest.raises(HTTPException) as exc_inactive:
        get_current_user(inactive)
    assert exc_inactive.value.status_code == 403

    active = User(id=3, username="active_user", hashed_password="x", role=Role.USER, is_active=True)
    assert get_current_user(active) == active


def test_get_admin_user_branches() -> None:
    normal = User(id=1, username="normal_user", hashed_password="x", role=Role.USER, is_active=True)
    with pytest.raises(HTTPException) as exc:
        get_admin_user(normal)
    assert exc.value.status_code == 403

    admin = User(id=2, username="admin", hashed_password="x", role=Role.ADMIN, is_active=True)
    assert get_admin_user(admin) == admin


def test_jwt_decode_invalid_raises() -> None:
    with pytest.raises(JWTError):
        JWTHandler().decode_token("invalid")


def test_jwt_create_with_custom_expiry() -> None:
    token = JWTHandler().create_access_token({"sub": "u"}, expires_delta=timedelta(minutes=1))
    payload = JWTHandler().decode_token(token)
    assert payload["sub"] == "u"
    assert "exp" in payload


def test_cloudinary_adapter_upload_calls_uploader() -> None:
    adapter = CloudinaryAdapter()
    with patch("infrastructure.adapters.cloudinary_adapter.cloudinary.uploader.upload") as upload:
        upload.return_value = {"secure_url": "https://res.cloudinary.com/test/image.jpg"}
        url = adapter.upload_image(b"binary", "test_id")

    assert url == "https://res.cloudinary.com/test/image.jpg"


def test_cloudinary_adapter_get_existing_url_found() -> None:
    adapter = CloudinaryAdapter()
    with patch("infrastructure.adapters.cloudinary_adapter.cloudinary.api.resource") as resource:
        resource.return_value = {"secure_url": "https://res.cloudinary.com/test/existing.jpg"}
        url = adapter.get_existing_url("car_1")

    assert url == "https://res.cloudinary.com/test/existing.jpg"


def test_cloudinary_adapter_get_existing_url_not_found() -> None:
    adapter = CloudinaryAdapter()
    with patch(
        "infrastructure.adapters.cloudinary_adapter.cloudinary.api.resource",
        side_effect=cloudinary.exceptions.NotFound("missing"),
    ):
        url = adapter.get_existing_url("car_missing")

    assert url is None
