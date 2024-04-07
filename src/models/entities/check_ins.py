from src.models.settings.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

class CheckIns(Base):
    __tablename__ = 'check_ins'
    id = Column(Integer, primary_key= True, nullable= False)
    created_at = Column(DateTime, default=func.now(), nullable= False)
    attendeeId = Column(String, ForeignKey("attendees.id"))
    
    def __repr__(self):
        return f"CheckIns [attendeeId: {self.attendeeId}]"