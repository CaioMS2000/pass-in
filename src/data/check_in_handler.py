import uuid
from src.models.repository.check_ins_repository import CheckInRepository
from src.http_types.http_request import HTTPRequest
from src.http_types.http_response import HTTPResponse

class CheckInHandler:
    def __init__(self) -> None:
        self.__check_in_repository = CheckInRepository()
        
    def registry(self, http_request: HTTPRequest) -> HTTPResponse:
        check_in_infos = http_request.param["attendee_id"]
        self.__check_in_repository.inser_check_in(check_in_infos)
        
        return HTTPResponse(body= None, status_code= 201)