from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    # RELIABILITY: Probes connections before use — drops stale connections
    # that were closed by the DB server after idle timeout.
    pool_pre_ping=True,
    # RELIABILITY: Recycle connections older than 5 minutes to prevent
    # "server closed the connection unexpectedly" errors on long-idle servers.
    pool_recycle=300,
    # PERFORMANCE: Connection pool configuration.
    # pool_size = persistent connections kept open.
    # max_overflow = extra connections allowed during bursts.
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
