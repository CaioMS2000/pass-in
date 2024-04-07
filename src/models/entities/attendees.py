from src.models.settings.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

class Attendees(Base):
    __tablename__ = 'attendees'
    id = Column(String, primary_key= True, nullable= False)
    name = Column(String, nullable= False)
    email = Column(String, nullable= False)
    created_at = Column(DateTime, default=func.now(), nullable= False)
    event_id = Column(String, ForeignKey("events.id"), nullable= False)
    
    def __repr__(self):
        return f"Attendees [id={self.id}, name={self.name}, email={self.email}, created_at={self.created_at}, event_id={self.event_id}]"
    