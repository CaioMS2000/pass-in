package devcaio.com.br.passin.services;

import devcaio.com.br.passin.domain.attendee.Attendee;
import devcaio.com.br.passin.domain.checkin.CheckIn;
import devcaio.com.br.passin.domain.checkin.exceptions.CheckInAlreadyExistsException;
import devcaio.com.br.passin.repositories.CheckinRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class CheckInService {
    private final CheckinRepository checkinRepository;

    private void verifyCheckInExixts(String attendeeId){
        Optional<CheckIn> isCheckedIn = this.checkinRepository.findByAttendeeId(attendeeId);

        if(isCheckedIn.isPresent()) throw new CheckInAlreadyExistsException("Attendee already checked in");
    }

    public void registerCheckIn(Attendee attendee) {
        this.verifyCheckInExixts(attendee.getId());
        CheckIn newCheckIn = new CheckIn();

        newCheckIn.setAttendee(attendee);
        newCheckIn.setCreatedAt(LocalDateTime.now());

        this.checkinRepository.save(newCheckIn);
    }

    public Optional<CheckIn> getCheckIn(String attendeeId){
        return this.checkinRepository.findByAttendeeId(attendeeId);
    }
}
