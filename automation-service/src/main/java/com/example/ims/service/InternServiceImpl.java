package com.example.ims.service;

import com.example.ims.model.Intern;
import com.example.ims.repository.InternRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class InternServiceImpl implements InternService {

    private final InternRepository internRepository;

    public InternServiceImpl(InternRepository internRepository) {
        this.internRepository = internRepository;
    }

    @Override
    public Intern registerIntern(Intern intern) {
        intern.setStatus("PENDING");
        return internRepository.save(intern);
    }

    @Override
    public List<Intern> getAllInterns() {
        return internRepository.findAll();
    }

    @Override
    public Intern getInternById(Long id) {
        return internRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Intern not found with id: " + id));
    }

    @Override
    public Intern evaluateIntern(Long id) {

        Intern intern = getInternById(id);

        if (intern.getScore() == null) {
            throw new RuntimeException("Score not assigned");
        }

        if (intern.getScore() >= 60) {
            intern.setStatus("PASSED");
        } else {
            intern.setStatus("FAILED");
        }

        return internRepository.save(intern);
    }

    @Override
    public void deleteIntern(Long id) {
        Intern intern = getInternById(id);
        internRepository.delete(intern);
    }
}