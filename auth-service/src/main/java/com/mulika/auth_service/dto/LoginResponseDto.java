package com.mulika.auth_service.dto;

public record LoginResponseDto(
        String token ,
        String email,
        String fullName
) {

}
