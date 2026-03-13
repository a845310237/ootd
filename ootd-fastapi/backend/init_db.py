"""Database initialization script."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from app.core.config import settings


def init_database():
    """Initialize database by creating all tables."""
    from app.core.database import Base
    from app.models.user import User
    from app.models.clothing import Clothing
    from app.models.outfit import Outfit, OutfitItem

    print(f"Connecting to database: {settings.DATABASE_URL}")

    # Create database engine
    engine = create_engine(settings.DATABASE_URL)

    # Import all models to ensure they're registered
    print("Creating tables...")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully!")
    print("\nCreated tables:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")


if __name__ == "__main__":
    init_database()
