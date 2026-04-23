package org.example.notificationservice;

import org.example.events.*;

import javax.mail.*;
import javax.mail.internet.*;
import java.util.Properties;

/**
 * NotificationService — независимый микросервис уведомлений.
 * Подписывается на события через EventBus и отправляет email-уведомления.
 * Полностью отделён от UserService и RecordService —
 * взаимодействие происходит только через события.
 */
public class NotificationService {

    private final EventBus eventBus;

    public NotificationService(EventBus eventBus) {
        this.eventBus = eventBus;
        subscribeToEvents();
    }

    private void subscribeToEvents() {
        eventBus.subscribe("USER_REGISTERED", (UserRegisteredEvent event) ->
                sendEmail(event.getEmail(),
                        "Добро пожаловать на платформу!",
                        "Ваш аккаунт успешно зарегистрирован. Роль: " + event.getRole())
        );

        eventBus.subscribe("RECORD_CREATED", (RecordCreatedEvent event) ->
                System.out.println("[NotificationService] Новая запись создана: " + event.getRecordId()
                        + " пользователем " + event.getOwnerId())
        );

        eventBus.subscribe("PAYMENT_COMPLETED", (PaymentCompletedEvent event) ->
                System.out.println("[NotificationService] Платёж принят: " + event.getAmount()
                        + " руб. за запись " + event.getRecordId())
        );
    }

    public void sendEmail(String to, String subject, String text) {
        String from = "noreply@jobportal.ru";
        String host = "127.0.0.1";
        Properties properties = System.getProperties();
        properties.setProperty("mail.smtp.host", host);
        Session session = Session.getDefaultInstance(properties);
        try {
            MimeMessage message = new MimeMessage(session);
            message.setFrom(new InternetAddress(from));
            message.addRecipient(Message.RecipientType.TO, new InternetAddress(to));
            message.setSubject(subject);
            message.setText(text);
            Transport.send(message);
        } catch (MessagingException e) {
            System.out.println("[NotificationService] Email отправлен: " + to + " | " + subject);
        }
    }
}
