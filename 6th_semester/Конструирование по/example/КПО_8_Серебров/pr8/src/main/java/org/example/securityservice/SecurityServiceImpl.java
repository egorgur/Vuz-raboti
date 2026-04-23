package org.example.securityservice;

import org.example.events.EventBus;
import org.example.events.UserRegisteredEvent;
import org.example.userservice.model.User;
import org.example.userservice.repository.UserRepository;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.util.UUID;

/**
 * SecurityService — отдельный микросервис безопасности.
 * Отвечает только за аутентификацию, авторизацию и шифрование.
 * После регистрации публикует событие UserRegisteredEvent в EventBus,
 * что позволяет другим сервисам (NotificationService) реагировать
 * без прямой зависимости от SecurityService.
 */
public class SecurityServiceImpl implements SecurityService {

    private static final String SECRET_KEY = "a1b2c3d4e5f6g7h8";
    private static final String ALGORITHM = "AES";

    private final UserRepository userRepository;
    private final EventBus eventBus;

    public SecurityServiceImpl(UserRepository userRepository, EventBus eventBus) {
        this.userRepository = userRepository;
        this.eventBus = eventBus;
    }

    @Override
    public boolean hasRole(String userId, String role) {
        User user = userRepository.findById(userId);
        if (user == null) return false;
        String userRole = decrypt(user.getEncryptedRole());
        return role.equalsIgnoreCase(userRole);
    }

    @Override
    public String authenticate(String email, String password) {
        User user = userRepository.findByEmail(email);
        if (user == null) return null;
        String storedHash = decrypt(user.getEncryptedPasswordHash());
        boolean valid = org.mindrot.jbcrypt.BCrypt.checkpw(password, storedHash);
        return valid ? generateToken(user.getId()) : null;
    }

    @Override
    public String registerUser(String email, String password, String role) {
        String userId = UUID.randomUUID().toString();
        String hash = org.mindrot.jbcrypt.BCrypt.hashpw(password, org.mindrot.jbcrypt.BCrypt.gensalt(12));

        User newUser = new User();
        newUser.setId(userId);
        newUser.setEncryptedEmail(encrypt(email));
        newUser.setEncryptedPasswordHash(encrypt(hash));
        newUser.setEncryptedRole(encrypt(role));

        userRepository.save(newUser);

        eventBus.publish(new UserRegisteredEvent(userId, email, role));

        return generateToken(userId);
    }

    @Override
    public boolean authorizeAction(String userId, String requiredRole) {
        if (!hasRole(userId, requiredRole)) {
            userRepository.logSecurityEvent(userId, "ACCESS_DENIED", requiredRole);
            return false;
        }
        return true;
    }

    private String generateToken(String userId) {
        String rawToken = userId + ":" + System.currentTimeMillis() + ":" + UUID.randomUUID();
        return encrypt(rawToken);
    }

    private String encrypt(String data) {
        try {
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            SecretKeySpec key = new SecretKeySpec(SECRET_KEY.getBytes(), ALGORITHM);
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte[] encrypted = cipher.doFinal(data.getBytes());
            return Base64.getEncoder().encodeToString(encrypted);
        } catch (Exception e) {
            throw new SecurityException("Encryption failed", e);
        }
    }

    private String decrypt(String encryptedData) {
        try {
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            SecretKeySpec key = new SecretKeySpec(SECRET_KEY.getBytes(), ALGORITHM);
            cipher.init(Cipher.DECRYPT_MODE, key);
            byte[] decoded = Base64.getDecoder().decode(encryptedData);
            byte[] decrypted = cipher.doFinal(decoded);
            return new String(decrypted);
        } catch (Exception e) {
            throw new SecurityException("Decryption failed", e);
        }
    }
}
