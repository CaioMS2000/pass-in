from .events_repository import EventsRepository
from src.models.settings.connection import db_connection_handler
from pytest import mark

db_connection_handler.connect_to_db()

@mark.skip(reason= "Novo registro")
def test_insert_event():
    event = {
        'id': 'SOME_UUID',
        'title': 'Title-test',
        'slug': 'slug-test',
        'maximum_attendees': 10,
    }
    
    events_repository = EventsRepository()
    response = events_repository.insert_event(event)
    
    print(response)

def test_get_event_by_id():
    event_id = 'SOME_UUID'
    events_repository = EventsRepository()
    response = events_repository.get_event_by_id(event_id)
    
    print(response)