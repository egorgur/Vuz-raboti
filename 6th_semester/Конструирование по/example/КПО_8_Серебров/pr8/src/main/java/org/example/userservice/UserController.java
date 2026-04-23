package org.example.userservice;

import org.example.securityservice.SecurityService;

/**
 * UserController — часть UserService.
 * Принимает HTTP-запросы, делегирует бизнес-логику SecurityService.
 * Не зависит напрямую от RecordService, AdminService и т.д.
 * Взаимодействие с другими сервисами происходит только через EventBus.
 */
public class UserController {

    private final SecurityService securityService;

    public UserController(SecurityService securityService) {
        this.securityService = securityService;
    }

    public String login(String email, String password) {
        return securityService.authenticate(email, password);
    }

    public String register(String email, String password, String role) {
        return securityService.registerUser(email, password, role);
    }

    public boolean canAccessResource(String userId, String resourceRole) {
        return securityService.authorizeAction(userId, resourceRole);
    }
}
