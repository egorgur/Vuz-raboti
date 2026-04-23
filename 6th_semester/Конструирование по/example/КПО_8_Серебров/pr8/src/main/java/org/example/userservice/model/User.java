package org.example.userservice.model;

public class User {
    private String id;
    private String encryptedEmail;
    private String encryptedPasswordHash;
    private String encryptedRole;

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getEncryptedEmail() { return encryptedEmail; }
    public void setEncryptedEmail(String encryptedEmail) { this.encryptedEmail = encryptedEmail; }

    public String getEncryptedPasswordHash() { return encryptedPasswordHash; }
    public void setEncryptedPasswordHash(String encryptedPasswordHash) { this.encryptedPasswordHash = encryptedPasswordHash; }

    public String getEncryptedRole() { return encryptedRole; }
    public void setEncryptedRole(String encryptedRole) { this.encryptedRole = encryptedRole; }
}
