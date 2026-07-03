package com.mulika.auth_service;

import com.mulika.auth_service.controller.UserController;
import com.mulika.auth_service.entity.User;
import com.mulika.auth_service.repository.UserRepository;
import com.mulika.auth_service.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.Optional;

@Slf4j
@SpringBootApplication
public class AuthServiceApplication{

	public static void main(String[] args) {

		SpringApplication.run(AuthServiceApplication.class, args);


	}



}

