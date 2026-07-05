package com.mulika.auth_service.dto;

public record LoginRequestDto(
        String email,
        String password
) {

}
