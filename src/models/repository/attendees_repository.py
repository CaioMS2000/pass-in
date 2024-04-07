from typing import Dict, List
from sqlalchemy.exc import IntegrityError, NoResultFound
from src.models.settings.connection import db_connection_handler
from src.models.entities.attendees import Attendees
from src.models.entities.events import Events
from src.models.entities.check_ins import CheckIns
from src.errors.error_types.http_conflict import HTTPConflictError

class AttendeesRepository:
    def inser_attendee(self, attendee_info: Dict) -> Dict:
        with db_connection_handler as database, database.get_session() as db_session:
            try:
                attendee = (Attendees(id= attendee_info.get('id'), name= attendee_info.get('name'), email= attendee_info.get('email'), event_id= attendee_info.get('event_id')))
                db_session.add(attendee)
                db_session.commit()
                
                return attendee_info
            
            except IntegrityError as error:
                print(error.orig)
                raise HTTPConflictError('Participante já cadastrado')
            
            except Exception as exception:
                db_session.rollback()
                
                raise exception
    
    def get_attendee_badge_by_id(self, attendee_id: str):
        with db_connection_handler as database, database.get_session() as db_session:
            try:
                attendee = (db_session.query(Attendees).join(Events, Events.id == Attendees.event_id).filter(Attendees.id == attendee_id).with_entities(Attendees.name, Attendees.email, Events.title).one())
                
                return attendee
                
            except NoResultFound:
                return None
            
            except Exception as exception:
                db_session.rollback()
                            
                raise exception
    
    def get_attendees_by_event_id(self, event_id: str) -> List[Attendees]:
        with db_connection_handler as database, database.get_session() as db_session:
            attendees = (db_session.query(Attendees).outerjoin(CheckIns, CheckIns.attendeeId == Attendees.id).filter(Attendees.event_id == event_id).with_entities(Attendees.id, Attendees.name, Attendees.email, CheckIns.created_at.label('checkInAt'), Attendees.created_at.label('createdAt')).all())
            
            return attendees
