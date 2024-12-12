

import java.util.HashMap;
import java.util.Map;

public class AuthenticationService {

    // Simulated user database with hardcoded username and password
    private static Map<String, String> userDatabase = new HashMap<>();
    
    static {
        // In a real application, you would store hashed passwords, not plaintext
        userDatabase.put("user1", "password123");

    }

    public static boolean authenticate(String username, String password) {
        // In a real application, you would retrieve the hashed password from the database
        String storedPassword = userDatabase.get(username);

        // Check if the username exists in the database and the password matches
        if (storedPassword != null && storedPassword.equals(password)) {
            return true; // Authentication successful
        } else {
            return false; // Authentication failed
        }
    }

    public static void main(String[] args) {
        // Example usage
        String username = "" ;
        String password = "" ;

        if (authenticate(username, password)) {
            System.out.println("Authentication successful.");
        } else {
            System.out.println("Authentication failed.");
        }
    }
    
}
