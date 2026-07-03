package com.plantcare.plantcare.service;

import com.plantcare.plantcare.entity.User;
import com.plantcare.plantcare.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public User getUserById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));
    }

    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(normalizeEmail(email));
    }

    public Optional<User> findByUserName(String userName) {
        return userRepository.findByUserName(normalizeUserName(userName));
    }

    @Transactional
    public User register(User user) {
        String email = normalizeEmail(user.getEmail());
        String userName = normalizeUserName(user.getUserName());
        String password = user.getPassword();

        if (email == null || email.isBlank()) {
            throw new IllegalArgumentException("Email is required");
        }
        if (userName == null || userName.isBlank()) {
            throw new IllegalArgumentException("Username is required");
        }
        if (password == null || password.isBlank()) {
            throw new IllegalArgumentException("Password is required");
        }
        if (password.length() < 6) {
            throw new IllegalArgumentException("Password must be at least 6 characters");
        }
        if (userRepository.existsByEmail(email)) {
            throw new IllegalArgumentException("Email is already in use");
        }
        if (userRepository.existsByUserName(userName)) {
            throw new IllegalArgumentException("Username is already in use");
        }

        user.setEmail(email);
        user.setUserName(userName);
        user.setPassword(passwordEncoder.encode(password));
        user.setCreatedAt(LocalDateTime.now());

        return userRepository.save(user);
    }

    public User authenticate(String email, String rawPassword) {
        User user = findByEmail(email)
                .orElseThrow(() -> new RuntimeException("Invalid email or password"));

        if (!passwordEncoder.matches(rawPassword, user.getPassword())) {
            throw new RuntimeException("Invalid email or password");
        }

        return user;
    }

    @Transactional
    public User updateUser(Long id, User updatedUser) {
        User user = getUserById(id);

        String email = normalizeEmail(updatedUser.getEmail());
        String userName = normalizeUserName(updatedUser.getUserName());

        if (email == null || email.isBlank()) {
            throw new IllegalArgumentException("Email is required");
        }
        if (userName == null || userName.isBlank()) {
            throw new IllegalArgumentException("Username is required");
        }

        if (!email.equals(user.getEmail()) && userRepository.existsByEmail(email)) {
            throw new IllegalArgumentException("Email is already in use");
        }
        if (!userName.equals(user.getUserName()) && userRepository.existsByUserName(userName)) {
            throw new IllegalArgumentException("Username is already in use");
        }

        user.setEmail(email);
        user.setUserName(userName);

        return userRepository.save(user);
    }

    @Transactional
    public void changePassword(Long id, String oldPassword, String newPassword) {
        User user = getUserById(id);

        if (newPassword == null || newPassword.isBlank()) {
            throw new IllegalArgumentException("New password is required");
        }
        if (newPassword.length() < 6) {
            throw new IllegalArgumentException("Password must be at least 6 characters");
        }
        if (!passwordEncoder.matches(oldPassword, user.getPassword())) {
            throw new IllegalArgumentException("Current password is incorrect");
        }

        user.setPassword(passwordEncoder.encode(newPassword));
        userRepository.save(user);
    }

    @Transactional
    public void deleteUser(Long id) {
        if (!userRepository.existsById(id)) {
            throw new RuntimeException("User not found");
        }
        userRepository.deleteById(id);
    }

    private String normalizeEmail(String email) {
        return email == null ? null : email.trim().toLowerCase();
    }

    private String normalizeUserName(String userName) {
        return userName == null ? null : userName.trim();
    }
}
