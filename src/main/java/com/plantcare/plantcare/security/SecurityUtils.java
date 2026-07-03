package com.plantcare.plantcare.security;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

public final class SecurityUtils {

    private SecurityUtils() {
    }

    public static UserPrincipal getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof UserPrincipal principal)) {
            throw new RuntimeException("User is not authenticated");
        }
        return principal;
    }

    public static Long getCurrentUserId() {
        return getCurrentUser().getUser().getId();
    }
}
