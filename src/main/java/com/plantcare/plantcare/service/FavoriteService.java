package com.plantcare.plantcare.service;

import com.plantcare.plantcare.dto.AddFavoriteRequest;
import com.plantcare.plantcare.dto.FavoriteResponse;
import com.plantcare.plantcare.entity.Favorite;
import com.plantcare.plantcare.entity.Plant;
import com.plantcare.plantcare.entity.User;
import com.plantcare.plantcare.repository.FavoriteRepository;
import com.plantcare.plantcare.repository.PlantRepository;
import com.plantcare.plantcare.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

@Service
public class FavoriteService {

    private final FavoriteRepository favoriteRepository;
    private final UserRepository userRepository;
    private final PlantRepository plantRepository;

    public FavoriteService(
            FavoriteRepository favoriteRepository,
            UserRepository userRepository,
            PlantRepository plantRepository
    ) {
        this.favoriteRepository = favoriteRepository;
        this.userRepository = userRepository;
        this.plantRepository = plantRepository;
    }

    public List<FavoriteResponse> getFavorites(Long userId) {
        return favoriteRepository.findByUser_IdOrderByDateAddedDesc(userId).stream()
                .map(FavoriteResponse::from)
                .toList();
    }

    @Transactional
    public FavoriteResponse addFavorite(Long userId, AddFavoriteRequest request) {
        if (favoriteRepository.existsByUser_IdAndPlant_Id(userId, request.getPlantId())) {
            throw new IllegalArgumentException("Plant is already in favorites");
        }

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        Plant plant = plantRepository.findById(request.getPlantId())
                .orElseThrow(() -> new RuntimeException("Plant not found"));

        Favorite favorite = new Favorite();
        favorite.setUser(user);
        favorite.setPlant(plant);
        favorite.setDateAdded(LocalDate.now());

        return FavoriteResponse.from(favoriteRepository.save(favorite));
    }

    @Transactional
    public void removeFavorite(Long userId, Long plantId) {
        if (!favoriteRepository.existsByUser_IdAndPlant_Id(userId, plantId)) {
            throw new RuntimeException("Favorite not found");
        }
        favoriteRepository.deleteByUser_IdAndPlant_Id(userId, plantId);
    }
}
