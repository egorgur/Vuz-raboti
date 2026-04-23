package org.example.adminservice;

import org.example.recordservice.repository.RecordRepository;
import org.example.securityservice.SecurityService;
import org.example.userservice.repository.UserRepository;

/**
 * AdminController — часть AdminService.
 * Предоставляет административные операции: удаление пользователей и записей.
 * Зависит от SecurityService для проверки прав ADMIN,
 * и от репозиториев UserService и RecordService через их публичные API.
 */
public class AdminController {

    private final UserRepository userRepository;
    private final RecordRepository recordRepository;
    private final SecurityService securityService;

    public AdminController(UserRepository userRepo,
                           RecordRepository recordRepo,
                           SecurityService security) {
        this.userRepository = userRepo;
        this.recordRepository = recordRepo;
        this.securityService = security;
    }

    public void deleteUser(String adminId, String targetUserId) {
        if (!securityService.authorizeAction(adminId, "ADMIN")) {
            throw new SecurityException("Admin access required");
        }
        userRepository.deleteById(targetUserId);
        System.out.println("[AdminService] Пользователь удалён: " + targetUserId);
    }

    public void deleteRecord(String adminId, String recordId) {
        if (!securityService.authorizeAction(adminId, "ADMIN")) {
            throw new SecurityException("Admin access required");
        }
        recordRepository.deleteRecord(recordId);
        System.out.println("[AdminService] Запись удалена: " + recordId);
    }
}
