package org.example.userservice.repository;

import org.example.userservice.model.User;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.sql.*;
import java.util.Base64;

/**
 * UserRepository — репозиторий данных UserService.
 * Каждый микросервис владеет своей собственной схемой базы данных
 * , что обеспечивает независимое
 * масштабирование и развёртывание.
 */
public class UserRepository {

    private static final String SECRET_KEY = "0123456789abcdef";
    private static final String ALGORITHM = "AES";
    private Connection connection;

    public UserRepository(Connection connection) {
        this.connection = connection;
    }

    public void save(User user) {
        try {
            String sql = "INSERT INTO users (id, email, password_hash, role) VALUES (?, ?, ?, ?)";
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, user.getId());
            stmt.setString(2, user.getEncryptedEmail());
            stmt.setString(3, user.getEncryptedPasswordHash());
            stmt.setString(4, user.getEncryptedRole());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public User findById(String userId) {
        try {
            String sql = "SELECT * FROM users WHERE id = ?";
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, userId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return mapRow(rs);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public User findByEmail(String email) {
        try {
            String encryptedEmail = encrypt(email);
            String sql = "SELECT * FROM users WHERE email = ?";
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, encryptedEmail);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return mapRow(rs);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public void deleteById(String userId) {
        try {
            String sql = "DELETE FROM users WHERE id = ?";
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, userId);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void logSecurityEvent(String userId, String eventType, String details) {
        try {
            String sql = "INSERT INTO security_log (user_id, event_type, details, created_at) VALUES (?, ?, ?, NOW())";
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, userId);
            stmt.setString(2, eventType);
            stmt.setString(3, details);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private User mapRow(ResultSet rs) throws SQLException {
        User user = new User();
        user.setId(rs.getString("id"));
        user.setEncryptedEmail(rs.getString("email"));
        user.setEncryptedPasswordHash(rs.getString("password_hash"));
        user.setEncryptedRole(rs.getString("role"));
        return user;
    }

    private String encrypt(String data) throws Exception {
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        SecretKeySpec key = new SecretKeySpec(SECRET_KEY.getBytes(), ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] encrypted = cipher.doFinal(data.getBytes());
        return Base64.getEncoder().encodeToString(encrypted);
    }
}
