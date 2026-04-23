package org.example.recordservice.model;

public abstract class JobRecord {
    private String id;
    Object nonSpecificData;

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public void setNonSpecificData(Object nonSpecificData) {
        this.nonSpecificData = nonSpecificData;
    }

    public Object getNonSpecificData() {
        return nonSpecificData;
    }
}
