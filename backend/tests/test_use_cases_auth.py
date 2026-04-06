from application.use_cases.auth_use_cases import AuthUseCases
from domain.entities.user import Role, User
from infrastructure.persistence.in_memory_user_repository import InMemoryUserRepository


def _auth_uc() -> AuthUseCases:
    repo = InMemoryUserRepository()
    repo.create(
        User(
            id=1,
            username="active",
            hashed_password=AuthUseCases.hash_password("secret"),
            role=Role.USER,
            is_active=True,
        )
    )
    repo.create(
        User(
            id=2,
            username="inactive",
            hashed_password=AuthUseCases.hash_password("secret"),
            role=Role.USER,
            is_active=False,
        )
    )
    return AuthUseCases(repo)


def test_authenticate_user_success() -> None:
    uc = _auth_uc()
    user = uc.authenticate_user("active", "secret")
    assert user is not None
    assert user.username == "active"


def test_authenticate_user_wrong_password() -> None:
    uc = _auth_uc()
    assert uc.authenticate_user("active", "wrong") is None


def test_authenticate_user_inactive_or_missing() -> None:
    uc = _auth_uc()
    assert uc.authenticate_user("inactive", "secret") is None
    assert uc.authenticate_user("missing", "secret") is None


def test_hash_password_generates_bcrypt_hash() -> None:
    hashed = AuthUseCases.hash_password("abc123")
    assert hashed != "abc123"
    assert hashed.startswith("$2")


def test_get_user_by_username_and_id() -> None:
    uc = _auth_uc()

    assert uc.get_user_by_username("active") is not None
    assert uc.get_user_by_username("missing") is None
    assert uc.get_user_by_id(1) is not None
    assert uc.get_user_by_id(999) is None
