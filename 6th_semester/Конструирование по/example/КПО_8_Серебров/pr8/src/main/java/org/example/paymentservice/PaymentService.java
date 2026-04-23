package org.example.paymentservice;

import org.example.events.EventBus;
import org.example.events.PaymentCompletedEvent;

public final class PaymentService {

    private static PaymentService instance;
    private final EventBus eventBus;

    private PaymentService(EventBus eventBus) {
        this.eventBus = eventBus;
    }

    public static synchronized PaymentService getInstance(EventBus eventBus) {
        if (instance == null) {
            instance = new PaymentService(eventBus);
        }
        return instance;
    }

    public boolean processPayment(String userId, String recordId, double amount) {
        boolean success = callExternalPaymentProvider(userId, amount);
        if (success) {
            eventBus.publish(new PaymentCompletedEvent(userId, recordId, amount));
        }
        return success;
    }

    private boolean callExternalPaymentProvider(String userId, double amount) {
        System.out.println("[PaymentService] Обработка платежа: " + amount + " руб. для " + userId);
        return true;
    }
}
