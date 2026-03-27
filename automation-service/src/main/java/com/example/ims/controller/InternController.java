package com.example.ims.controller;

import com.example.ims.model.Intern;
import com.example.ims.repository.InternRepository;
import com.example.ims.service.InternService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/interns")
public class InternController {

    private final InternRepository internRepository;
    private final InternService internService;

    public InternController(InternRepository internRepository,
                            InternService internService) {
        this.internRepository = internRepository;
        this.internService = internService;
    }

    //  Get all interns
    @GetMapping
    public List<Intern> getAllInterns() {
        return internRepository.findAll();
    }

    //  Get intern by ID
    @GetMapping("/{id}")
    public ResponseEntity<Intern> getInternById(@PathVariable Long id) {
        return internRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    //  Register new intern
    @PostMapping
    public ResponseEntity<Intern> registerIntern(@RequestBody Intern intern) {
        Intern savedIntern = internRepository.save(intern);
        return ResponseEntity.ok(savedIntern);
    }

    // Evaluate intern
    @PutMapping("/evaluate/{id}")
    public ResponseEntity<Intern> evaluateIntern(@PathVariable Long id) {
        try {
            Intern evaluatedIntern = internService.evaluateIntern(id);
            return ResponseEntity.ok(evaluatedIntern);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    // Delete intern
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteIntern(@PathVariable Long id) {
        if (internRepository.existsById(id)) {
            internRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }
}