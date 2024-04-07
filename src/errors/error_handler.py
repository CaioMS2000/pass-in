from src.http_types.http_response import HTTPResponse
from .error_types.http_not_found import HTTPNotFoundError
from .error_types.http_conflict import HTTPConflictError

def handle_error(error: Exception) -> HTTPResponse:
    if isinstance(error, (HTTPNotFoundError, HTTPConflictError)):
        return HTTPResponse(body={"errors": [{"title": error.name, "details": error.message}]}, status_code= error.status_code)
    
    return HTTPResponse(body={"errors": [{"title": "error", "details": str(error)}]})