from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def init_db(db_uri):
    engine = create_engine(db_uri)
    try:
        with engine.connect() as conn:
            yield sessionmaker(conn)
            conn.commit()
    finally:
        engine.dispose()
