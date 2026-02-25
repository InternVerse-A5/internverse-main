package com.example.automated;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AutomatedServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(AutomatedServiceApplication.class, args);
        System.out.println("Automated Service Application started successfully!");
    }
}