package com.plantcare.plantcare.dto;

import com.plantcare.plantcare.entity.Plant;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class PlantResponse {

    private Long id;
    private String name;
    private String wateringRecomendation;
    private String lightningRecomendation;
    private String transferInformation;
    private String poisonInformation;
    private String optionalInfoCare;
    private String imagePath;

    public static PlantResponse from(Plant plant) {
        PlantResponse response = new PlantResponse();
        response.setId(plant.getId());
        response.setName(plant.getName());
        response.setWateringRecomendation(plant.getWateringRecomendation());
        response.setLightningRecomendation(plant.getLightningRecomendation());
        response.setTransferInformation(plant.getTransferInformation());
        response.setPoisonInformation(plant.getPoisonInformation());
        response.setOptionalInfoCare(plant.getOptionalInfoCare());
        response.setImagePath(plant.getImagePath());
        return response;
    }
}
