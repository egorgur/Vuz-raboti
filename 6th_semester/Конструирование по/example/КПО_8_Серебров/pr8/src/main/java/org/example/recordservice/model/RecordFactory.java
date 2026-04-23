package org.example.recordservice.model;

public abstract class RecordFactory {
    public JobRecord createRecord(Object nonSpecificData, Object specificData) {
        JobRecord record = getRecordWithNonSpecificData(nonSpecificData);
        record = getRecordWithSpecificData(record, specificData);
        return record;
    }

    public abstract JobRecord getRecordWithNonSpecificData(Object nonSpecificData);
    public abstract JobRecord getRecordWithSpecificData(JobRecord record, Object specificData);
}
