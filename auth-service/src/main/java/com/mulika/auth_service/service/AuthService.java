package com.mulika.auth_service.service;


import com.mulika.auth_service.dto.RegisterRequestDto;
import com.mulika.auth_service.dto.RegisterResponseDto;
import com.mulika.auth_service.entity.User;
import com.mulika.auth_service.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepo;

    private final PasswordEncoder passwordEncoder;

    private boolean emailExists(String email){
        return userRepo.findByEmail(email).isPresent();
    }

    public RegisterResponseDto register( RegisterRequestDto request){
        if (emailExists(request.email())){
            throw new RuntimeException("Email Already Exists ");
        }
        String hashPassword = passwordEncoder.encode(request.password());

        User user = new User();

        user.setFullName(request.fullName());
        user.setEmail(request.email());
        user.setPasswordHash(hashPassword);
        user.setActive(true);

        User saved = userRepo.save(user);
        return new RegisterResponseDto(saved.getId(),saved.getEmail(),saved.getFullName());
    }
}
