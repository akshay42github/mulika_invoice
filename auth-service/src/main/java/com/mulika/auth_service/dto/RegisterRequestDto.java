package com.mulika.auth_service.dto;

public record RegisterRequestDto(
        String fullName,
        String email,
        String password

){ }