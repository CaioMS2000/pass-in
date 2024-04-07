from typing import Dict
from sqlalchemy.exc import IntegrityError, NoResultFound
from src.models.settings.connection import db_connection_handler
from src.models.entities.check_ins import CheckIns
from src.errors.error_types.http_conflict import HTTPConflictError

class CheckInRepository:
    def inser_check_in(self, attendee_id: str) -> str:
        with db_connection_handler as database, database.get_session() as db_session:
            try:
                checdk_in = (CheckIns(attendeeId= attendee_id))
                db_session.add(checdk_in)
                db_session.commit()
                
                return attendee_id
            
            except IntegrityError as error:
                print(error.orig)
                raise HTTPConflictError('CheckIn já cadastrado')
            
            except Exception as exception:
                db_session.rollback()
                
                raise exception