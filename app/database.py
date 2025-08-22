from sqlmodel import create_engine, SQLModel, Session
from pathlib import Path
import os

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{data_dir}/portal.db")

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)


def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session


def init_database():
    """Initialize database with default data"""
    from app.models import StandardHours, Settings
    import yaml
    from datetime import datetime
    
    create_db_and_tables()
    
    # Load config
    with open('config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    with Session(engine) as session:
        # Check if already initialized
        existing = session.query(Settings).filter_by(key="initialized").first()
        if existing:
            return
        
        # Create standard hours from config
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        for i, day in enumerate(days):
            hours = StandardHours(
                day_of_week=i,
                time_ranges=config['hours']['weekly'].get(day, [])
            )
            session.add(hours)
        
        # Mark as initialized
        session.add(Settings(
            key="initialized",
            value={"date": datetime.utcnow().isoformat()}
        ))
        
        # Store site config
        session.add(Settings(
            key="site_config",
            value=config
        ))
        
        session.commit()