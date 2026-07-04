package com.plantcare.plantcare.service;

import com.plantcare.plantcare.dto.AddUserPlantRequest;
import com.plantcare.plantcare.dto.UpdateUserPlantRequest;
import com.plantcare.plantcare.dto.UserPlantResponse;
import com.plantcare.plantcare.entity.Plant;
import com.plantcare.plantcare.entity.User;
import com.plantcare.plantcare.entity.UserPlant;
import com.plantcare.plantcare.repository.PlantRepository;
import com.plantcare.plantcare.repository.UserPlantRepository;
import com.plantcare.plantcare.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

@Service
public class UserPlantService {

    private final UserPlantRepository userPlantRepository;
    private final UserRepository userRepository;
    private final PlantRepository plantRepository;

    public UserPlantService(
            UserPlantRepository userPlantRepository,
            UserRepository userRepository,
            PlantRepository plantRepository
    ) {
        this.userPlantRepository = userPlantRepository;
        this.userRepository = userRepository;
        this.plantRepository = plantRepository;
    }

    public List<UserPlantResponse> getUserPlants(Long userId) {
        return userPlantRepository.findByUser_IdOrderByDateAddedDesc(userId).stream()
                .map(UserPlantResponse::from)
                .toList();
    }

    @Transactional
    public UserPlantResponse addUserPlant(Long userId, AddUserPlantRequest request) {
        if (userPlantRepository.existsByUser_IdAndPlant_Id(userId, request.getPlantId())) {
            throw new IllegalArgumentException("Plant is already in your collection");
        }

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        Plant plant = plantRepository.findById(request.getPlantId())
                .orElseThrow(() -> new RuntimeException("Plant not found"));

        validateReminderDays(request.getWateringReminderDays());
        validateReminderDays(request.getTransferReminderDays());

        UserPlant userPlant = new UserPlant();
        userPlant.setUser(user);
        userPlant.setPlant(plant);
        userPlant.setDateAdded(LocalDate.now());
        userPlant.setNotes(normalizeNotes(request.getNotes()));
        userPlant.setWateringReminderDays(request.getWateringReminderDays());
        userPlant.setTransferReminderDays(request.getTransferReminderDays());

        return UserPlantResponse.from(userPlantRepository.save(userPlant));
    }

    @Transactional
    public UserPlantResponse updateUserPlant(Long userId, Long id, UpdateUserPlantRequest request) {
        UserPlant userPlant = userPlantRepository.findByIdAndUser_Id(id, userId)
                .orElseThrow(() -> new RuntimeException("User plant not found"));

        if (request.getNotes() != null) {
            userPlant.setNotes(normalizeNotes(request.getNotes()));
        }
        if (request.getWateringReminderDays() != null) {
            validateReminderDays(request.getWateringReminderDays());
            userPlant.setWateringReminderDays(request.getWateringReminderDays());
        }
        if (request.getTransferReminderDays() != null) {
            validateReminderDays(request.getTransferReminderDays());
            userPlant.setTransferReminderDays(request.getTransferReminderDays());
        }
        if (request.getLastWateredAt() != null) {
            userPlant.setLastWateredAt(request.getLastWateredAt());
        }
        if (request.getLastTransferredAt() != null) {
            userPlant.setLastTransferredAt(request.getLastTransferredAt());
        }

        return UserPlantResponse.from(userPlantRepository.save(userPlant));
    }

    @Transactional
    public void removeUserPlant(Long userId, Long id) {
        if (!userPlantRepository.findByIdAndUser_Id(id, userId).isPresent()) {
            throw new RuntimeException("User plant not found");
        }
        userPlantRepository.deleteByIdAndUser_Id(id, userId);
    }

    private void validateReminderDays(Integer days) {
        if (days != null && days < 1) {
            throw new IllegalArgumentException("Reminder interval must be at least 1 day");
        }
    }

    private String normalizeNotes(String notes) {
        if (notes == null) {
            return null;
        }
        String trimmed = notes.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }
}
