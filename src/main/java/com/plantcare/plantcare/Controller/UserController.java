package com.plantcare.plantcare.Controller;

import com.plantcare.plantcare.dto.ChangePasswordRequest;
import com.plantcare.plantcare.dto.UpdateUserRequest;
import com.plantcare.plantcare.dto.UserResponse;
import com.plantcare.plantcare.entity.User;
import com.plantcare.plantcare.security.SecurityUtils;
import com.plantcare.plantcare.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/me")
    public ResponseEntity<UserResponse> getProfile() {
        User user = userService.getUserById(SecurityUtils.getCurrentUserId());
        return ResponseEntity.ok(UserResponse.from(user));
    }

    @PutMapping("/me")
    public ResponseEntity<UserResponse> updateProfile(@Valid @RequestBody UpdateUserRequest request) {
        User updatedUser = new User();
        updatedUser.setUserName(request.getUserName());
        updatedUser.setEmail(request.getEmail());

        User user = userService.updateUser(SecurityUtils.getCurrentUserId(), updatedUser);
        return ResponseEntity.ok(UserResponse.from(user));
    }

    @PutMapping("/me/password")
    public ResponseEntity<Void> changePassword(@Valid @RequestBody ChangePasswordRequest request) {
        userService.changePassword(
                SecurityUtils.getCurrentUserId(),
                request.getOldPassword(),
                request.getNewPassword()
        );
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/me")
    public ResponseEntity<Void> deleteAccount() {
        userService.deleteUser(SecurityUtils.getCurrentUserId());
        return ResponseEntity.noContent().build();
    }
}
