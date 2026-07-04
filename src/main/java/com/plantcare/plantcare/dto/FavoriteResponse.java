package com.plantcare.plantcare.dto;

import com.plantcare.plantcare.entity.Favorite;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class FavoriteResponse {

    private Long id;
    private Long plantId;
    private LocalDate dateAdded;
    private PlantResponse plant;

    public static FavoriteResponse from(Favorite favorite) {
        FavoriteResponse response = new FavoriteResponse();
        response.setId(favorite.getId());
        response.setPlantId(favorite.getPlant().getId());
        response.setDateAdded(favorite.getDateAdded());
        response.setPlant(PlantResponse.from(favorite.getPlant()));
        return response;
    }
}
