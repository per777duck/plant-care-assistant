package com.plantcare.plantcare.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter @Setter
@Table(name="users")
public class User {
    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
        private long id;
    @Column(name="user_name")
        private String userName;
    @Column(unique = true, nullable = false)
        private String email;
    @Column(nullable = false,length = 60)
        private String password;
    @Column(name = "created_at", nullable = false, updatable = false)
        private LocalDateTime createdAt;
}
