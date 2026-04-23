package org.example.events;

import java.time.Instant;
import java.util.UUID;

public abstract class Event {
    private final String eventId;
    private final Instant occurredAt;

    protected Event() {
        this.eventId = UUID.randomUUID().toString();
        this.occurredAt = Instant.now();
    }

    public String getEventId() {
        return eventId;
    }

    public Instant getOccurredAt() {
        return occurredAt;
    }

    public abstract String getEventType();
}
