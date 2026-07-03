package com.mulika.auth_service.dto;

import java.util.UUID;

public record RegisterResponseDto (
        UUID id,
        String email,
        String fullName
){ }
