package com.plantcare.plantcare.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AddFavoriteRequest {

    @NotNull
    private Long plantId;
}
