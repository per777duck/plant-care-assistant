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
    @PostMapping
    public Plant addPlant(@RequestBody Plant plant) {
        return plantService.addPlant(plant);
    }
}
