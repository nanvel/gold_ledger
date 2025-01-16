from app.models import User, UserRole
from app.repos.users import UsersRepo


def test_users(session):
    repo = UsersRepo(session)
    user_id = repo.create(
        User(
            username="test",
            password_hash="password",
            role=UserRole.EMPLOYEE,
            token_version=0,
            id=0,
        )
    )

    user = repo.by_id(user_id)

    assert user.id == user_id
    assert user.username == "test"
    assert user.password_hash == "password"
    assert user.role == UserRole.EMPLOYEE
    assert user.token_version == 0
