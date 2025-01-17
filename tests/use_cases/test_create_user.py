from app.models import UserRole


def test_create_user(container):
    container.create_user()(username="admin", password="pass", role=99)

    with container.uow() as uow:
        user = uow.users.by_username("admin")

    assert user.username == "admin"
    assert user.role == UserRole.ADMIN
