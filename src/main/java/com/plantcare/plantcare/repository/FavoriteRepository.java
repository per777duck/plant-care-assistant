package com.plantcare.plantcare.repository;

import com.plantcare.plantcare.entity.Favorite;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface FavoriteRepository extends JpaRepository<Favorite, Long> {

    @EntityGraph(attributePaths = "plant")
    List<Favorite> findByUser_IdOrderByDateAddedDesc(Long userId);

    @EntityGraph(attributePaths = "plant")
    Optional<Favorite> findByUser_IdAndPlant_Id(Long userId, Long plantId);

    boolean existsByUser_IdAndPlant_Id(Long userId, Long plantId);

    void deleteByUser_IdAndPlant_Id(Long userId, Long plantId);
}
