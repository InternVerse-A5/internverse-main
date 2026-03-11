package com.example.internverse.emailservice.controlller;

import com.example.internverse.emailservice.model.EmailRequest;
import com.example.internverse.emailservice.service.EmailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/email")
public class EmailController {

    @Autowired
    private EmailService emailService;

    @PostMapping("/send")
    public String sendEmail(@RequestBody EmailRequest request) {

        emailService.sendEmail(request);

        return "Email Sent Successfully";
    }
}