package devcaio.com.br.passin.config;

import devcaio.com.br.passin.domain.attendee.exceptions.AttendeeAlreadyExistException;
import devcaio.com.br.passin.domain.attendee.exceptions.AttendeeNotFoundException;
import devcaio.com.br.passin.domain.checkin.exceptions.CheckInAlreadyExistsException;
import devcaio.com.br.passin.domain.event.exceptions.EventFullException;
import devcaio.com.br.passin.domain.event.exceptions.EventNotFoundException;
import devcaio.com.br.passin.dto.general.ErrorResponseDTO;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class ExceptionEntityHandler {
    @ExceptionHandler(EventNotFoundException.class)
    public ResponseEntity handleEventNotFound(EventNotFoundException exception){
        exception.getCause();
        return ResponseEntity.notFound().build();
    }

    @ExceptionHandler(AttendeeNotFoundException.class)
    public ResponseEntity handleAttendeeNotFound(EventNotFoundException exception){
        exception.getCause();
        return ResponseEntity.notFound().build();
    }

    @ExceptionHandler(AttendeeAlreadyExistException.class)
    public ResponseEntity handleAttendeeAlreadyExistNotFound(EventNotFoundException exception){
        exception.getCause();
        return ResponseEntity.status(HttpStatus.CONFLICT).build();
    }

    @ExceptionHandler(CheckInAlreadyExistsException.class)
    public ResponseEntity handleCheckInAlreadyExists(EventNotFoundException exception){
        exception.getCause();
        return ResponseEntity.status(HttpStatus.CONFLICT).build();
    }

    @ExceptionHandler(EventFullException.class)
    public ResponseEntity handleEventFull(EventNotFoundException exception){
        exception.getCause();
        return ResponseEntity.badRequest().body(new ErrorResponseDTO(exception.getMessage()));
    }
}
