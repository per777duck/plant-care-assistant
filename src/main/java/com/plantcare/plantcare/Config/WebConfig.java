package com.plantcare.plantcare.Config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.nio.file.Path;
import java.nio.file.Paths;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOriginPatterns("*")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true);
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        String root = Paths.get("").toAbsolutePath().toUri().toString();

        registry.addResourceHandler("/layouts/**")
                .addResourceLocations(root + "layouts/");
        registry.addResourceHandler("/scripts/**")
                .addResourceLocations(root + "scripts/");
        registry.addResourceHandler("/styles/**")
                .addResourceLocations(root + "styles/");
        registry.addResourceHandler("/images/**")
                .addResourceLocations(
                        "classpath:/static/images/",
                        root + "images/"
                );
    }
}
