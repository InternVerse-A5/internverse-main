package com.example.internverse.emailservice.service;

import com.example.internverse.emailservice.model.EmailRequest;

public interface EmailService {

    void sendEmail(String to, String subject, String body);

    void sendEmail(EmailRequest request);

}