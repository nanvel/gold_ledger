from app.models import User
from app.repos.users import UsersRepo


def test_users(session):
    repo = UsersRepo(session)
    user_id = repo.create(
        User(
            username="test",
            password_hash="password",
            token_version=0,
            id=0,
            supplier_id=None,
            retailer_id=None,
        )
    )

    user = repo.by_id(user_id)

    assert user.id == user_id
    assert user.username == "test"
    assert user.password_hash == "password"
    assert user.token_version == 0
