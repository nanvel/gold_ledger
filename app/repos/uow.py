from .users import UsersRepo


class UnitOfFork:
    users: UsersRepo

    def __init__(self, db):
        self._db = db
        self._session = None

    def __enter__(self):
        self._session = self._db()
        self._session.begin()
        self.users = UsersRepo(self._session)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()

        self._session.close()
