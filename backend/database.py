"""
SQLAlchemy database engine, session factory, and declarative base.
Tables are auto-created on application startup.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# connect_args needed only for SQLite (allows multi-threaded access)
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables():
    """Called on app startup to create all tables if they don't exist."""
    # Import models here so they register with Base before create_all
    import models.user          # noqa: F401
    import models.profile       # noqa: F401
    import models.resume_history  # noqa: F401
    Base.metadata.create_all(bind=engine)
