package org.example.events;

public class UserRegisteredEvent extends Event {
    private final String userId;
    private final String email;
    private final String role;

    public UserRegisteredEvent(String userId, String email, String role) {
        super();
        this.userId = userId;
        this.email = email;
        this.role = role;
    }

    public String getUserId() { return userId; }
    public String getEmail()  { return email; }
    public String getRole()   { return role; }

    @Override
    public String getEventType() { return "USER_REGISTERED"; }
}
