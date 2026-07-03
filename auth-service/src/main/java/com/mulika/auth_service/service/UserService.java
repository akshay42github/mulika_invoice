package com.mulika.auth_service.service;

import com.mulika.auth_service.entity.User;
import com.mulika.auth_service.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepo;

    public Optional<User> findByEmail(String email){
        return userRepo.findByEmail(email);
    }

}
