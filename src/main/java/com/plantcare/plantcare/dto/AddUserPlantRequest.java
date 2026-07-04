package com.plantcare.plantcare.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AddUserPlantRequest {

    @NotNull
    private Long plantId;

    private String notes;

    private Integer wateringReminderDays;

    private Integer transferReminderDays;
}
