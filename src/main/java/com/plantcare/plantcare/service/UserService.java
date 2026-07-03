package com.plantcare.plantcare.service;

import com.plantcare.plantcare.entity.Plant;
import com.plantcare.plantcare.repository.PlantRepository;
import com.plantcare.plantcare.repository.UserRepository;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
//    public Plant getUserById(Long id) {
//        return userRepository.findById(id)
//                .orElseThrow(() -> new RuntimeException("Plant not found"));
//    }

}
