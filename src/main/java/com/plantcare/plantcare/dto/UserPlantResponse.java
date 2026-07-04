package com.plantcare.plantcare.dto;

import com.plantcare.plantcare.entity.UserPlant;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class UserPlantResponse {

    private Long id;
    private Long plantId;
    private LocalDate dateAdded;
    private String notes;
    private Integer wateringReminderDays;
    private Integer transferReminderDays;
    private LocalDate lastWateredAt;
    private LocalDate lastTransferredAt;
    private PlantResponse plant;

    public static UserPlantResponse from(UserPlant userPlant) {
        UserPlantResponse response = new UserPlantResponse();
        response.setId(userPlant.getId());
        response.setPlantId(userPlant.getPlant().getId());
        response.setDateAdded(userPlant.getDateAdded());
        response.setNotes(userPlant.getNotes());
        response.setWateringReminderDays(userPlant.getWateringReminderDays());
        response.setTransferReminderDays(userPlant.getTransferReminderDays());
        response.setLastWateredAt(userPlant.getLastWateredAt());
        response.setLastTransferredAt(userPlant.getLastTransferredAt());
        response.setPlant(PlantResponse.from(userPlant.getPlant()));
        return response;
    }
}
