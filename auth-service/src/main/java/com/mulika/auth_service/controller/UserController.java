package com.mulika.auth_service.controller;

import com.mulika.auth_service.entity.User;
import com.mulika.auth_service.service.UserService;

import lombok.RequiredArgsConstructor;

import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@CrossOrigin("*")
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {


    private final UserService service;

    @GetMapping
    public Optional<User> getUserFromEmail(@RequestParam String email){
        return service.findByEmail(email);

    }
}
