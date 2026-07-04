package com.plantcare.plantcare.dto;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class UpdateUserPlantRequest {

    private String notes;

    private Integer wateringReminderDays;

    private Integer transferReminderDays;

    private LocalDate lastWateredAt;

    private LocalDate lastTransferredAt;
}
