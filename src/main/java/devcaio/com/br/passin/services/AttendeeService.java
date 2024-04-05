package devcaio.com.br.passin.services;

import devcaio.com.br.passin.domain.attendee.Attendee;
import devcaio.com.br.passin.domain.attendee.exceptions.AttendeeAlreadyExistException;
import devcaio.com.br.passin.domain.attendee.exceptions.AttendeeNotFoundException;
import devcaio.com.br.passin.domain.checkin.CheckIn;
import devcaio.com.br.passin.dto.attendee.AttendeeBadgeResponseDTO;
import devcaio.com.br.passin.dto.attendee.AttendeeDetails;
import devcaio.com.br.passin.dto.attendee.AttendeesListResponseDTO;
import devcaio.com.br.passin.dto.attendee.AttendeeBadgeDTO;
import devcaio.com.br.passin.repositories.AttendeeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.util.UriComponentsBuilder;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class AttendeeService {
    private final AttendeeRepository attendeeRepository;
    private final CheckInService checkInService;

    private Attendee getAttendee(String attendeeId){
        return this.attendeeRepository.findById(attendeeId).orElseThrow(() -> new AttendeeNotFoundException("Attendee with id " + attendeeId + " not found"));
    }

    public List<Attendee> getAllAttendeesFromEvent(String eventId){
        return this.attendeeRepository.findByEventId(eventId);
    }

    public AttendeesListResponseDTO getEventsAttendee(String eventId){
        List<Attendee> attendeeList = this.getAllAttendeesFromEvent(eventId);
        List<AttendeeDetails> attendeeDetailsList = attendeeList.stream().map(attendee -> {
            Optional<CheckIn> checkIn = this.checkInService.getCheckIn(attendee.getId());
//            LocalDateTime checkedInAt = checkIn.isPresent()? checkIn.get().getCreatedAt() : null;
            LocalDateTime checkedInAt = checkIn.<LocalDateTime>map(CheckIn::getCreatedAt).orElse(null);

            return new AttendeeDetails(attendee.getId(), attendee.getName(), attendee.getEmail(), attendee.getCreatedAt(), checkedInAt);
        }).toList();

        return new AttendeesListResponseDTO(attendeeDetailsList);
    }

    public Attendee registerAttendee(Attendee newAttendee){
        this.attendeeRepository.save(newAttendee);
        return newAttendee;
    }

    public void verifyAttendeeSubscription(String email, String eventId){
        Optional<Attendee> isAttendeeRegistred = this.attendeeRepository.findByEventIdAndEmail(eventId, email);
        if(isAttendeeRegistred.isPresent()) throw new AttendeeAlreadyExistException("** Attendee already registred **");
    }

    public AttendeeBadgeResponseDTO getAttendeeBadge(String attendeeId, UriComponentsBuilder uriComponentsBuilder){
        Attendee attendee = this.getAttendee(attendeeId);
        var uri = uriComponentsBuilder.path("/attendees/{id}/check-in").buildAndExpand(attendeeId).toUri().toString();

        return new AttendeeBadgeResponseDTO(new AttendeeBadgeDTO(attendee.getName(), attendee.getEmail(), uri, attendee.getEvent().getId()));
    }

    public void checkInAttendee(String attendeeId){
        Attendee attendee = this.getAttendee(attendeeId);
        this.checkInService.registerCheckIn(attendee);
    }
}
