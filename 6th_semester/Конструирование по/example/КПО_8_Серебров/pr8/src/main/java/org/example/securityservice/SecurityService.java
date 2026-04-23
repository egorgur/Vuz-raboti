package org.example.securityservice;

public interface SecurityService {
    boolean hasRole(String userId, String role);
    String authenticate(String email, String password);
    String registerUser(String email, String password, String role);
    boolean authorizeAction(String userId, String requiredRole);
}
