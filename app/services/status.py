from datetime import date, datetime
from typing import Optional
from sqlmodel import Session, select
from app.models import Status, StatusType
from app.database import engine


class StatusService:
    @staticmethod
    def get_current_status() -> Optional[Status]:
        """Get the current active status"""
        with Session(engine) as session:
            # Get latest status
            statement = select(Status).order_by(Status.created_at.desc())
            status = session.exec(statement).first()
            
            if not status:
                # Create default status if none exists
                status = Status(type=StatusType.ANWESEND)
                session.add(status)
                session.commit()
                session.refresh(status)
            
            # Check if status is still valid
            today = date.today()
            if status.date_to and status.date_to < today:
                # Status expired, set to present
                status = Status(type=StatusType.ANWESEND)
                session.add(status)
                session.commit()
                session.refresh(status)
            
            return status
    
    @staticmethod
    def update_status(
        status_type: StatusType,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        description: Optional[str] = None,
        next_return: Optional[date] = None
    ) -> Status:
        """Update the current status"""
        with Session(engine) as session:
            status = Status(
                type=status_type,
                date_from=date_from,
                date_to=date_to,
                description=description,
                next_return=next_return,
                updated_at=datetime.utcnow()
            )
            session.add(status)
            session.commit()
            session.refresh(status)
            return status
    
    @staticmethod
    def is_available() -> bool:
        """Check if currently available"""
        status = StatusService.get_current_status()
        return status.type == StatusType.ANWESEND if status else True