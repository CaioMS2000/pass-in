from .attendees_repository import AttendeesRepository
from src.models.settings.connection import db_connection_handler
from pytest import mark

db_connection_handler.connect_to_db()

@mark.skip(reason= "Novo registro")
def test_inser_attendee():
    event_id = "SOME_UUID"
    attendee_info = {
        "id": "SOME_UUID",
        "name": "name-test",
        "email": "email-test",
        "event_id": event_id,
    }
    
    attendees_repository = AttendeesRepository()
    response = attendees_repository.inser_attendee(attendee_info)
    
    print(response)

@mark.skip(reason= "...")
def test_get_attendee_badge_by_id():
    attendee_id = "SOME_UUID"
    attendees_repository = AttendeesRepository()
    response = attendees_repository.get_attendee_badge_by_id(attendee_id)
    
    print(response)