package com.plantcare.plantcare.Controller;

import com.plantcare.plantcare.dto.AddUserPlantRequest;
import com.plantcare.plantcare.dto.UpdateUserPlantRequest;
import com.plantcare.plantcare.dto.UserPlantResponse;
import com.plantcare.plantcare.security.SecurityUtils;
import com.plantcare.plantcare.service.UserPlantService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/user-plants")
public class UserPlantController {

    private final UserPlantService userPlantService;

    public UserPlantController(UserPlantService userPlantService) {
        this.userPlantService = userPlantService;
    }

    @GetMapping
    public List<UserPlantResponse> getUserPlants() {
        return userPlantService.getUserPlants(SecurityUtils.getCurrentUserId());
    }

    @PostMapping
    public ResponseEntity<UserPlantResponse> addUserPlant(@Valid @RequestBody AddUserPlantRequest request) {
        UserPlantResponse response = userPlantService.addUserPlant(SecurityUtils.getCurrentUserId(), request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PutMapping("/{id}")
    public UserPlantResponse updateUserPlant(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserPlantRequest request
    ) {
        return userPlantService.updateUserPlant(SecurityUtils.getCurrentUserId(), id, request);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> removeUserPlant(@PathVariable Long id) {
        userPlantService.removeUserPlant(SecurityUtils.getCurrentUserId(), id);
        return ResponseEntity.noContent().build();
    }
}
