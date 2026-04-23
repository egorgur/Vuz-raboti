package org.example.recordservice;

import org.example.events.EventBus;
import org.example.events.PaymentCompletedEvent;
import org.example.events.RecordCreatedEvent;
import org.example.recordservice.model.*;
import org.example.recordservice.repository.RecordRepository;
import org.example.securityservice.SecurityService;

import java.util.UUID;

/**
 * RecordController — часть RecordService.
 * Управляет жизненным циклом вакансий и резюме.
 * После создания записи публикует событие RecordCreatedEvent,
 * после оплаты продвижения — PaymentCompletedEvent.
 * Это позволяет NotificationService реагировать без прямой зависимости.
 */
public class RecordController {

    private final RecordFactory recordFactory;
    private final RecordRepository recordRepository;
    private final SecurityService securityService;
    private final EventBus eventBus;

    public RecordController(RecordRepository repo, RecordType type,
                            SecurityService security, EventBus eventBus) {
        this.recordRepository = repo;
        this.securityService = security;
        this.eventBus = eventBus;
        this.recordFactory = (type == RecordType.VACANCY)
                ? new VacancyFactoryImpl()
                : new ResumeFactoryImpl();
    }

    public void registerRecord(String userId, Object nonSpecific, Object specific) {
        if (!securityService.authorizeAction(userId, "EMPLOYER")) {
            throw new SecurityException("Access denied: only employers can post records");
        }
        JobRecord record = recordFactory.createRecord(nonSpecific, specific);
        record.setId(UUID.randomUUID().toString());
        recordRepository.insertRecord(record);

        eventBus.publish(new RecordCreatedEvent(record.getId(), userId,
                record.getClass().getSimpleName()));
    }

    public void promoteRecord(String userId, JobRecord record) {
        if (!securityService.authorizeAction(userId, "EMPLOYER")) {
            throw new SecurityException("Access denied: only employers can promote records");
        }
        double promotionFee = 299.0;
        recordRepository.updateRecord(record);

        eventBus.publish(new PaymentCompletedEvent(userId, record.getId(), promotionFee));
    }
}
