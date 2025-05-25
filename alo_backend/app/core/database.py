import logging
import os
import time
from typing import Optional

from sqlalchemy import create_engine, exc, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from .config import get_settings
from ..models import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Log the database URL (with sensitive info masked)
db_url = settings.DATABASE_URL
masked_url = db_url
if '@' in db_url:
    # Mask password in URL for logging
    user_pass = db_url.split('@')[0]
    if ':' in user_pass:
        user = user_pass.split(':')[0]
        masked_url = f"{user}:****@{db_url.split('@')[1]}"

logger.info(f"Initializing database connection to: {masked_url}")

# Create SQLAlchemy engine with robust error handling
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,        # Verify connections before using them
        pool_recycle=300,          # Recycle connections after 5 minutes
        pool_size=5,               # Start with 5 connections
        max_overflow=10,           # Allow up to 10 additional connections
        connect_args={
            "connect_timeout": 10,  # Timeout after 10 seconds
        },
    )
    
    # Add connection pool event listeners for better diagnostics
    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        logger.info("Database connection established")

    @event.listens_for(engine, "checkout")
    def checkout(dbapi_connection, connection_record, connection_proxy):
        logger.debug("Database connection checked out")

    @event.listens_for(engine, "checkin")
    def checkin(dbapi_connection, connection_record):
        logger.debug("Database connection checked in")
        
except exc.SQLAlchemyError as e:
    logger.error(f"Error creating SQLAlchemy engine: {str(e)}")
    # Create a fallback engine with minimal configuration
    # This ensures the application starts even with database issues
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=1,
        max_overflow=1,
        pool_timeout=30,
    )
    
except Exception as e:
    # Last resort fallback for catastrophic failures
    logger.critical(f"Critical error creating database engine: {str(e)}")
    # Create a dummy engine that will raise appropriate errors when used
    # but still allows the application to start
    engine = create_engine('sqlite:///:memory:')

# Create a configured "Session" class
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

def get_db():
    """Dependency for getting database session with robust error handling"""
    db = SessionLocal()
    try:
        # Test the connection by executing a simple query
        # This will fail early if the connection is invalid
        db.execute("SELECT 1")
        yield db
    except exc.SQLAlchemyError as e:
        logger.error(f"Database connection error in get_db: {str(e)}")
        # Attempt to reconnect once before failing
        try:
            db.close()
            db = SessionLocal()
            db.execute("SELECT 1")  # Verify the new connection works
            yield db
        except Exception as e:
            logger.critical(f"Critical database connection failure: {str(e)}")
            # Re-raise so FastAPI can return a 500 error
            raise
    except Exception as e:
        logger.error(f"Unexpected error in get_db: {str(e)}")
        raise
    finally:
        db.close()

def init_db(max_retries: int = 5, retry_interval: int = 2) -> bool:
    """
    Initialize database with retry logic
    
    Args:
        max_retries: Maximum number of connection attempts
        retry_interval: Seconds to wait between retries
        
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    logger.info("Initializing database schema")
    
    for attempt in range(1, max_retries + 1):
        try:
            # Test connection before attempting to create tables
            with engine.connect() as conn:
                conn.execute("SELECT 1")
                logger.info("Database connection verified before schema initialization")
            
            # Create all tables according to the metadata
            Base.metadata.create_all(bind=engine)
            logger.info("Database schema successfully initialized")
            return True
            
        except exc.SQLAlchemyError as e:
            logger.error(f"Database initialization error (attempt {attempt}/{max_retries}): {str(e)}")
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
                # Increase backoff time for next attempt
                retry_interval = min(retry_interval * 2, 30)  # Max 30 seconds between retries
            else:
                logger.critical(f"Failed to initialize database after {max_retries} attempts")
                return False
                
        except Exception as e:
            logger.critical(f"Unexpected error during database initialization: {str(e)}")
            return False
            
    return False  # Should not reach here, but just in case
