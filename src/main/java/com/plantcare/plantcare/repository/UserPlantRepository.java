package com.plantcare.plantcare.repository;

import com.plantcare.plantcare.entity.UserPlant;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface UserPlantRepository extends JpaRepository<UserPlant, Long> {

    @EntityGraph(attributePaths = "plant")
    List<UserPlant> findByUser_IdOrderByDateAddedDesc(Long userId);

    @EntityGraph(attributePaths = "plant")
    Optional<UserPlant> findByIdAndUser_Id(Long id, Long userId);

    boolean existsByUser_IdAndPlant_Id(Long userId, Long plantId);

    void deleteByIdAndUser_Id(Long id, Long userId);
}
