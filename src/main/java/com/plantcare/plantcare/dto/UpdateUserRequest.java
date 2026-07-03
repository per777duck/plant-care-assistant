package com.plantcare.plantcare.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UpdateUserRequest {

    @NotBlank
    @Size(max = 50)
    private String userName;

    @NotBlank
    @Email
    private String email;
}
