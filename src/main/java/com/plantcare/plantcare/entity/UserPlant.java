package com.plantcare.plantcare.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;

import java.time.LocalDate;

@Entity
public class UserPlant {
    @Id
    @GeneratedValue
    private Long id;
    private Long plantId;
    private LocalDate dateAdded;
    private String notes;
    private Integer wateringReminderDays;
}
