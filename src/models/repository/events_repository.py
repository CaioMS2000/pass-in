from typing import Dict
from sqlalchemy.exc import IntegrityError, NoResultFound
from src.models.settings.connection import db_connection_handler
from src.models.entities.events import Events
from src.models.entities.attendees import Attendees
from src.errors.error_types.http_conflict import HTTPConflictError

class EventsRepository:
    def insert_event(self, events_info: Dict) -> Dict:
        with db_connection_handler as database, database.get_session() as db_session:
            try:

                event = Events(id= events_info.get('id'), title= events_info.get('title'), details= events_info.get('details'), slug= events_info.get('slug'), maximum_attendees= events_info.get('maximum_attendees'))
                db_session.add(event)
                db_session.commit()
                
                return events_info
            except IntegrityError as error:
                print(error.orig)
                raise HTTPConflictError('Evento já cadastrado')
            
            except Exception as exception:
                db_session.rollback()
                raise exception
    
    def get_event_by_id(self, event_id: str) -> Events:
        try:
            with db_connection_handler as database, database.get_session() as db_session:
                event = (db_session.query(Events).filter(Events.id == event_id).one())
                
                return event
        except NoResultFound:
            return None
    
    def count_event_attendees(self, event_id: str) -> Dict:
        with db_connection_handler as database, database.get_session() as db_session:
            event_count = (db_session.query(Events).join(Attendees, Events.id == Attendees.event_id).filter(Events.id == event_id).with_entities(Events.maximum_attendees, Attendees.id).all())
            if not len(event_count):
                return {"maximumAttendees": 0, "attendeesAmount": 0}
            
            return {"maximumAttendees": event_count[0].maximum_attendees, "attendeesAmount": len(event_count)}