package com.example.ims.service;

import com.example.ims.model.Intern;
import java.util.List;

public interface InternService {

    Intern registerIntern(Intern intern);

    List<Intern> getAllInterns();

    Intern getInternById(Long id);

    Intern evaluateIntern(Long id);

    void deleteIntern(Long id);
}