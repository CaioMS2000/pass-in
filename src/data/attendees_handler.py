import uuid
from src.models.repository.attendees_repository import AttendeesRepository
from src.models.repository.events_repository import EventsRepository
from src.http_types.http_request import HTTPRequest
from src.http_types.http_response import HTTPResponse
from src.errors.error_types.http_not_found import HTTPNotFoundError
from src.errors.error_types.http_conflict import HTTPConflictError

class AttendeesHandler:
    def __init__(self) -> None:
        self.__attendees_repository = AttendeesRepository()
        self.__events_repository = EventsRepository()
    
    def registry(self, http_request: HTTPRequest) -> HTTPResponse:
        body = http_request.body
        event_id = http_request.param["event_id"]
        event_attendees_count = self.__events_repository.count_event_attendees(event_id)
        
        if(event_attendees_count["attendeesAmount"] and event_attendees_count["maximumAttendees"] < event_attendees_count["attendeesAmount"]):
            raise HTTPConflictError("Evento lotado")
        
        body["id"] = str(uuid.uuid4())
        body["event_id"] = event_id
        
        self.__attendees_repository.inser_attendee(body)
        
        return HTTPResponse(body= None, status_code= 201)
    
    def find_attendee_badge(self, http_request: HTTPRequest) -> HTTPResponse:
        attendee_id = http_request.param["attendee_id"]
        badge = self.__attendees_repository.get_attendee_badge_by_id(attendee_id)
        
        if not badge: raise HTTPNotFoundError("Participante não encontrado")
        
        return HTTPResponse(body= {"badge": {"email": badge.email, "name": badge.name, "eventTitle": badge.title}}, status_code= 200)
    
    def find_attendees_from_event(self, http_request: HTTPRequest) -> HTTPResponse:
        event_id = http_request.param['event_id']
        attendees = self.__attendees_repository.get_attendees_by_event_id(event_id)
        
        if not attendees: raise HTTPNotFoundError("Participantes não encontrados")
        
        formatted_attendees = []
        
        for attendee in attendees:
            formatted_attendees.append({
                "id": attendee.id,
                "name": attendee.name,
                "email": attendee.email,
                "checkInAt": attendee.checkInAt,
                "createdAt": attendee.createdAt,
            })
        
        return HTTPResponse(body= {"attendees": formatted_attendees}, status_code= 200)
        