package org.example.events;

public class PaymentCompletedEvent extends Event {
    private final String userId;
    private final String recordId;
    private final double amount;

    public PaymentCompletedEvent(String userId, String recordId, double amount) {
        super();
        this.userId = userId;
        this.recordId = recordId;
        this.amount = amount;
    }

    public String getUserId()   { return userId; }
    public String getRecordId() { return recordId; }
    public double getAmount()   { return amount; }

    @Override
    public String getEventType() { return "PAYMENT_COMPLETED"; }
}
