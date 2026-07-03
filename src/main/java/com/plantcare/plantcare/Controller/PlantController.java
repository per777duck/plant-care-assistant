package com.plantcare.plantcare.Controller;

import com.plantcare.plantcare.entity.Plant;
import com.plantcare.plantcare.service.PlantService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/plants")
public class PlantController {

    private final PlantService plantService;

    public PlantController(PlantService plantService) {
        this.plantService = plantService;
    }

    @GetMapping
    public List<Plant> getAllPlants() {
        return plantService.getAllPlants();
    }

    @GetMapping("/{id}")
    public Plant getPlantById(@PathVariable Long id) {
        return plantService.getPlantById(id);
    }

    @PostMapping
    public Plant addPlant(@RequestBody Plant plant) {
        return plantService.addPlant(plant);
    }

    @PutMapping("/{id}")
    public Plant updatePlant(@PathVariable Long id,
                             @RequestBody Plant plant) {
        return plantService.updatePlant(id, plant);
    }

    @DeleteMapping("/{id}")
    public void deletePlant(@PathVariable Long id) {
        plantService.deletePlant(id);
    }

    @GetMapping("/search")
    public List<Plant> searchPlants(@RequestParam String name) {
        return plantService.searchPlants(name);
    }
}