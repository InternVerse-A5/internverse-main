package com.example.ims.model;

import jakarta.persistence.*;

@Entity
public class Intern {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String email;
    private String college;
    private Integer score;
    private String status;

    public Intern() {}

    public Intern(String name, String email, String college, Integer score) {
        this.name = name;
        this.email = email;
        this.college = college;
        this.score = score;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    public String getCollege() {
        return college;
    }

    public Integer getScore() {
        return score;
    }

    public String getStatus() {
        return status;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setCollege(String college) {
        this.college = college;
    }

    public void setScore(Integer score) {
        this.score = score;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}