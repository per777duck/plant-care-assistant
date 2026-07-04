package com.plantcare.plantcare.Controller;

import com.plantcare.plantcare.dto.AddFavoriteRequest;
import com.plantcare.plantcare.dto.FavoriteResponse;
import com.plantcare.plantcare.security.SecurityUtils;
import com.plantcare.plantcare.service.FavoriteService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/favorites")
public class FavoriteController {

    private final FavoriteService favoriteService;

    public FavoriteController(FavoriteService favoriteService) {
        this.favoriteService = favoriteService;
    }

    @GetMapping
    public List<FavoriteResponse> getFavorites() {
        return favoriteService.getFavorites(SecurityUtils.getCurrentUserId());
    }

    @PostMapping
    public ResponseEntity<FavoriteResponse> addFavorite(@Valid @RequestBody AddFavoriteRequest request) {
        FavoriteResponse response = favoriteService.addFavorite(SecurityUtils.getCurrentUserId(), request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @DeleteMapping("/{plantId}")
    public ResponseEntity<Void> removeFavorite(@PathVariable Long plantId) {
        favoriteService.removeFavorite(SecurityUtils.getCurrentUserId(), plantId);
        return ResponseEntity.noContent().build();
    }
}
