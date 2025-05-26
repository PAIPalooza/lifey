import logging
import os
import time
from typing import Optional, Tuple

from sqlalchemy import create_engine, exc, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.pool import QueuePool

from .config import get_settings
from ..models import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to enable lazy initialization
engine = None
SessionLocal = None

# Improve performance by deferring database initialization
def initialize_database(force: bool = False) -> Tuple[Engine, scoped_session]:
    """Lazy initialization of database connection
    
    This function implements lazy initialization of the database connection to improve
    the startup time of the application, particularly when accessing documentation endpoints.
    
    Args:
        force: Force reinitialization even if already initialized
        
    Returns:
        tuple: (engine, session_factory)
    """
    global engine, SessionLocal
    
    # Only initialize once unless forced
    if engine is not None and SessionLocal is not None and not force:
        return engine, SessionLocal
    
    # Get application settings
    settings = get_settings()
    
    # Log initialization start
    logger.info("Lazy database initialization starting")
    
    # Check if this is a Railway.com deployment with placeholder URL or malformed URL
    db_url = settings.DATABASE_URL
    use_fallback = False
    
    # Handle the case where Railway.com includes the variable name in the value
    # Example: 'DATABASE_URL=postgresql://postgres:postgres@localhost:5432/alodb'
    if db_url.startswith('DATABASE_URL='):
        logger.warning("Detected variable name in DATABASE_URL value, stripping prefix")
        db_url = db_url.replace('DATABASE_URL=', '', 1)
        # Update the settings value as well
        settings.DATABASE_URL = db_url
        logger.info(f"Corrected DATABASE_URL format")
    
    # Detect Railway.com placeholder format
    if 'hostname' in db_url or 'port' in db_url:
        logger.warning("Detected Railway.com placeholder URL - using SQLite memory database as fallback")
        use_fallback = True
        # Don't log the actual URL as it contains placeholders
        masked_url = "Railway.com placeholder URL (using fallback)"
    else:
        # Standard URL masking for logging
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
        if use_fallback:
            # CRITICAL: Using in-memory SQLite as fallback when Railway provides placeholder URL
            # This allows the application to start and serve documentation
            # Note: This is not suitable for production data storage
            logger.warning("USING IN-MEMORY DATABASE - Application in documentation mode only")
            engine = create_engine(
                'sqlite:///:memory:',
                connect_args={'check_same_thread': False}
            )
        else:
            # Normal PostgreSQL engine creation
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
            
        # Create a configured "Session" class
        SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
        
        logger.info("Database initialization completed successfully")
        return engine, SessionLocal
        
    except exc.SQLAlchemyError as e:
        logger.error(f"Error creating SQLAlchemy engine: {str(e)}")
        # Create a fallback engine with minimal configuration
        engine = create_engine(
            'sqlite:///:memory:',
            connect_args={'check_same_thread': False}
        )
        SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
        return engine, SessionLocal
    
    except Exception as e:
        # Last resort fallback for catastrophic failures
        logger.critical(f"Critical error creating database engine: {str(e)}")
        # Create a dummy engine that will still allow the app to start
        engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
        SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
        return engine, SessionLocal

        # Create a configured "Session" class
        SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
        
        logger.info("Database initialization completed successfully")
        return engine, SessionLocal
        
    except exc.SQLAlchemyError as e:
        logger.error(f"Error creating SQLAlchemy engine: {str(e)}")
        # Create a fallback engine with minimal configuration
        engine = create_engine(
            'sqlite:///:memory:',
            connect_args={'check_same_thread': False}
        )
        SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
        return engine, SessionLocal
    
    except Exception as e:
        # Last resort fallback for catastrophic failures
        logger.critical(f"Critical error creating database engine: {str(e)}")
        # Create a dummy engine that will still allow the app to start
        engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
        SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
        return engine, SessionLocal


# Initialize database on startup if not in documentation-only mode
# Documentation endpoints set DEFER_DB_INIT=true to improve page load times
if os.environ.get('DEFER_DB_INIT') != 'true':
    engine, SessionLocal = initialize_database()

def get_db():
    """Dependency for getting database session with robust error handling
    
    This function is used as a FastAPI dependency to provide database sessions
    to API endpoints. It includes robust error handling and automatic reconnection.
    
    Yields:
        Session: A SQLAlchemy session for database operations
    """
    global SessionLocal
    
    # Ensure database is initialized using lazy initialization
    if SessionLocal is None:
        logger.info("Lazy initializing database on first use")
        _, SessionLocal = initialize_database()
    
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
            # Force reinitialization
            logger.info("Attempting to reinitialize database connection")
            _, SessionLocal = initialize_database(force=True)
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
    """Initialize database with retry logic

    Creates database tables with exponential backoff retry logic following
    ALO Project Development Rules section 11 (Error Handling).

    Args:
        max_retries: Maximum number of connection attempts
        retry_interval: Seconds to wait between retries

    Returns:
        bool: True if initialization was successful, False otherwise
    """
    global engine

    # Ensure engine is initialized
    if engine is None:
        engine, _ = initialize_database()

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


# Initialize database on startup if not in documentation-only mode
# Documentation endpoints set DEFER_DB_INIT=true to improve page load times
if os.environ.get('DEFER_DB_INIT') != 'true':
    initialize_database()
