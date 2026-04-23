package org.example.gateway;

import org.example.adminservice.AdminController;
import org.example.recordservice.RecordController;
import org.example.userservice.UserController;

/**
 * ApiGateway — единая точка входа для всех запросов клиентов.
 * Маршрутизирует запросы к соответствующим микросервисам.
 * Скрывает внутреннюю топологию системы от внешних клиентов.
 */
public class ApiGateway {

    private final UserController userController;
    private final RecordController recordController;
    private final AdminController adminController;

    public ApiGateway(UserController userController,
                      RecordController recordController,
                      AdminController adminController) {
        this.userController = userController;
        this.recordController = recordController;
        this.adminController = adminController;
    }

    public String handleLogin(String email, String password) {
        System.out.println("[ApiGateway] POST /auth/login -> UserService");
        return userController.login(email, password);
    }

    public String handleRegister(String email, String password, String role) {
        System.out.println("[ApiGateway] POST /auth/register -> UserService");
        return userController.register(email, password, role);
    }

    public void handleCreateRecord(String userId, Object nonSpecific, Object specific) {
        System.out.println("[ApiGateway] POST /records -> RecordService");
        recordController.registerRecord(userId, nonSpecific, specific);
    }

    public void handleDeleteUser(String adminId, String targetId) {
        System.out.println("[ApiGateway] DELETE /admin/users/" + targetId + " -> AdminService");
        adminController.deleteUser(adminId, targetId);
    }
}
