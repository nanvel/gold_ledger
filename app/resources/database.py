from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def init_db(db_uri):
    engine = create_engine(db_uri)
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            yield sessionmaker(conn)
            conn.commit()
    finally:
        engine.dispose()


def init_db_readonly(db_uri):
    engine = create_engine(db_uri)
    try:
        with engine.connect().execution_options(
            isolation_level="SERIALIZABLE",
            postgresql_readonly=True,
            postgresql_deferrable=True,
        ) as conn:
            yield conn
    finally:
        engine.dispose()
