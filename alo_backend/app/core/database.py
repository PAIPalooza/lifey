from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import get_settings
from ..models import Base

settings = get_settings()

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections after 5 minutes
    pool_size=5,
    max_overflow=10
)

# Create a configured "Session" class
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """
    Initialize the database by creating all tables.
    This should only be used for development and testing.
    For production, use migrations.
    """
    Base.metadata.create_all(bind=engine)
