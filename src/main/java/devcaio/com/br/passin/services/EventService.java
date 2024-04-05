package devcaio.com.br.passin.services;

import devcaio.com.br.passin.domain.attendee.Attendee;
import devcaio.com.br.passin.domain.event.Event;
import devcaio.com.br.passin.domain.event.exceptions.EventFullException;
import devcaio.com.br.passin.domain.event.exceptions.EventNotFoundException;
import devcaio.com.br.passin.dto.attendee.AttendeeIdDTO;
import devcaio.com.br.passin.dto.attendee.AttendeeRequestDTO;
import devcaio.com.br.passin.dto.event.EventIdDTO;
import devcaio.com.br.passin.dto.event.EventRequestDTO;
import devcaio.com.br.passin.dto.event.EventResponseDTO;
import devcaio.com.br.passin.repositories.EventRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.text.Normalizer;
import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class EventService {
    private final EventRepository eventRepository;
    private final AttendeeService attendeeService;

    private Event getEventById(String eventId){
        return this.eventRepository.findById(eventId)
                .orElseThrow(() -> new EventNotFoundException("** Event with id " + eventId + " not found **"));
    }

    private String createSlug(String text){
        String normalized = Normalizer.normalize(text, Normalizer.Form.NFD);

        return normalized.replaceAll("[\\p{InCOMBINING_DIACRITICAL_MARKS}]", "")
                .replaceAll("[^\\w\\s]", "")
                .replaceAll("\\s+", "")
                .toLowerCase();
    }

    public EventResponseDTO getEventDetail(String eventId) {
        Event event = getEventById(eventId);
        List<Attendee> attendeeList = this.attendeeService.getAllAttendeesFromEvent(eventId);
        return new EventResponseDTO(event, attendeeList.size());
    }

    public EventIdDTO createEvent(EventRequestDTO eventDTO){
        Event newEvent = new Event();
        newEvent.setTitle(eventDTO.title());
        newEvent.setDetails(eventDTO.details());
        newEvent.setMaximumAttendees(eventDTO.maximumAttendees());
        newEvent.setSlug(this.createSlug(eventDTO.title()));

        this.eventRepository.save(newEvent);

        return new EventIdDTO(newEvent.getId());
    }

    public AttendeeIdDTO registerAttendeeOnEvent(String eventId, AttendeeRequestDTO attendeeRequestDTO){
        this.attendeeService.verifyAttendeeSubscription(attendeeRequestDTO.email(), eventId);

        Event event = getEventById(eventId);
        List<Attendee> attendeeList = this.attendeeService.getAllAttendeesFromEvent(eventId);

        if(event.getMaximumAttendees() <= attendeeList.size()) throw new EventFullException("Event is full");

        Attendee newAttendee = new Attendee();
        newAttendee.setEmail(attendeeRequestDTO.email());
        newAttendee.setName(attendeeRequestDTO.name());
        newAttendee.setEvent(event);
        newAttendee.setCreatedAt(LocalDateTime.now());

        this.attendeeService.registerAttendee(newAttendee);

        return new AttendeeIdDTO(newAttendee.getId());
    }
}
