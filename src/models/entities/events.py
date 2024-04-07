from src.models.settings.base import Base
from sqlalchemy import Column, String, Integer

class Events(Base):
    __tablename__ = 'events'
    id = Column(String, primary_key= True, nullable= False)
    title = Column(String, nullable= False)
    details = Column(String)
    slug = Column(String, nullable= False)
    maximum_attendees = Column(Integer)
    
    # def __repr__(self):
    #     return f"Events [id={self.id}, title={self.title}, details={self.details}, slug={self.slug}, maximum_attendees={self.maximum_attendees}]"
    
    def __str__(self):
        return f"Events [id={self.id}, title={self.title}, details={self.details}, slug={self.slug}, maximum_attendees={self.maximum_attendees}]"