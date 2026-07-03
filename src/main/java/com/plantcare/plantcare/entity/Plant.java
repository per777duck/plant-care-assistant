package com.plantcare.plantcare.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter @Setter
@Table(name="plants")
public class Plant {
    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
        private long id;
    private String name;
    @Column(name="watering_recomendation")
        private String wateringRecomendation;
    @Column(name="lightning_recomendation")
        private String lightningRecomendation;
    @Column(name="transfer_information")
        private String transferInformation;
    @Column(name="poison_information")
        private String poisonInformation;
    @Column(name="optional_info_care")
        private String optionalInfoCare;
    @Column(name="image_path")
        private String imagePath;
}
