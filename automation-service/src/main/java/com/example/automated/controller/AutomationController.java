package com.example.automated.controller;

import com.example.automated.service.mail.EmailService;
import com.example.automated.service.pdf.CertificateService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/automation")
public class AutomationController {

    @Autowired
    private CertificateService certificateService;

    @Autowired
    private EmailService emailService;

    // Generate Certificate
    @GetMapping("/certificate")
    public ResponseEntity<byte[]> generateCertificate(@RequestParam String name) {

        byte[] pdfBytes = certificateService.generateCertificate(name);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=certificate.pdf")
                .contentType(MediaType.APPLICATION_PDF)
                .body(pdfBytes);
    }

    // Send Email
    @PostMapping("/send-email")
    public String sendEmail(@RequestParam String to) {

        emailService.sendEmail(
                to,
                "Welcome to Internship",
                "Congratulations on joining the internship program!"
        );

        return "Email sent successfully!";
    }
}