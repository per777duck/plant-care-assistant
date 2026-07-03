package com.plantcare.plantcare.service;

import com.plantcare.plantcare.entity.Plant;
import com.plantcare.plantcare.repository.PlantRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PlantService {

    private final PlantRepository plantRepository;

    public PlantService(PlantRepository plantRepository) {
        this.plantRepository = plantRepository;
    }

    public List<Plant> getAllPlants() {
        return plantRepository.findAll();
    }

    public Plant getPlantById(Long id) {
        return plantRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Plant not found"));
    }

    public Plant addPlant(Plant plant) {
        return plantRepository.save(plant);
    }

    public Plant updatePlant(Long id, Plant updatedPlant) {

        Plant plant = plantRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Plant not found"));

        plant.setName(updatedPlant.getName());
        plant.setWateringRecomendation(updatedPlant.getWateringRecomendation());
        plant.setLightningRecomendation(updatedPlant.getLightningRecomendation());
        plant.setTransferInformation(updatedPlant.getTransferInformation());
        plant.setPoisonInformation(updatedPlant.getPoisonInformation());
        plant.setOptionalInfoCare(updatedPlant.getOptionalInfoCare());

        return plantRepository.save(plant);
    }

    public void deletePlant(Long id) {
        plantRepository.deleteById(id);
    }
    public List<Plant> searchPlants(String name) {
        return plantRepository.findByNameContainingIgnoreCase(name);
    }
}