package com.example.automated.service.mail;

public interface EmailService {
    void sendEmail(String to, String subject, String text);
}