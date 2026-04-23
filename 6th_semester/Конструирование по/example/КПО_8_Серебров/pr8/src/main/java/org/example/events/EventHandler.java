package org.example.events;

public interface EventHandler<T extends Event> {
    void handle(T event);
}
