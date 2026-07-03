package com.mulika.auth_service.controller;

import com.mulika.auth_service.dto.RegisterRequestDto;
import com.mulika.auth_service.dto.RegisterResponseDto;
import com.mulika.auth_service.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

   @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequestDto request){
       return ResponseEntity.status(HttpStatus.CREATED).body(authService.register(request));
   }
}
