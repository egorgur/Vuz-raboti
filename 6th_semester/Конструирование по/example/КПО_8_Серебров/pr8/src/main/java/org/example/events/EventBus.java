package org.example.events;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * EventBus обеспечивает асинхронную слабосвязанную коммуникацию
 * между микросервисами через паттерн Publisher-Subscriber.
 * Заменяет прямые вызовы между слоями монолитного MVC.
 */
public class EventBus {

    private static EventBus instance;
    private final Map<String, List<EventHandler<? extends Event>>> handlers = new HashMap<>();

    private EventBus() {}

    public static synchronized EventBus getInstance() {
        if (instance == null) {
            instance = new EventBus();
        }
        return instance;
    }

    @SuppressWarnings("unchecked")
    public <T extends Event> void subscribe(String eventType, EventHandler<T> handler) {
        handlers.computeIfAbsent(eventType, k -> new ArrayList<>()).add(handler);
    }

    @SuppressWarnings("unchecked")
    public <T extends Event> void publish(T event) {
        List<EventHandler<? extends Event>> eventHandlers = handlers.getOrDefault(event.getEventType(), new ArrayList<>());
        for (EventHandler handler : eventHandlers) {
            handler.handle(event);
        }
    }
}
