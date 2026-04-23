package org.example.events;

public class RecordCreatedEvent extends Event {
    private final String recordId;
    private final String ownerId;
    private final String recordType;

    public RecordCreatedEvent(String recordId, String ownerId, String recordType) {
        super();
        this.recordId = recordId;
        this.ownerId = ownerId;
        this.recordType = recordType;
    }

    public String getRecordId()   { return recordId; }
    public String getOwnerId()    { return ownerId; }
    public String getRecordType() { return recordType; }

    @Override
    public String getEventType() { return "RECORD_CREATED"; }
}
