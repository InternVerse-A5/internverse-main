# InternVerse – MongoDB Connection Guide

## Overview

InternVerse uses **MongoDB Atlas (Cloud)** as the centralized database for all services.

Cluster Name: **A5**  
Database Name: **internverse**

This database is shared across microservices:

- Node.js (API Gateway)
- Python (Analytics Service)
- Java (Automation Service)

Each service has its own dedicated database user for security.

---

# Database Structure

Database: `internverse`

Collections:

- `users`
- `tasks`
- `analytics`

---

# Service-Level Database Users

| Service        | Username         |
| -------------- | ---------------- |
| Node Service   | `node_service`   |
| Python Service | `python_service` |
| Java Service   | `java_service`   |

Each user has:
-readWrite access to internverse database only

No access to:

- admin
- config
- local
- any other database

---

# Connection String Template

mongodb+srv://<username>:<password>@a5.lyeaaef.mongodb.net/internverse?appName=A5

---

# How to Set Up Connection (All Services)

## Step 1 — Create `.env` File

In your project root:
.env
Add:
MONGO_URI=mongodb+srv://<username>:<password>@a5.lyeaaef.mongodb.net/internverse?appName=A5

---

# Python Service Setup (FastAPI / Flask)

## Install Dependencies

```bash
pip install pymongo python-dotenv
```

Create db.py

```bash
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["internverse"]

users = db["users"]
tasks = db["tasks"]
analytics = db["analytics"]
```

Test Connection

```bash
print(db.list_collection_names())
```

Expected Output:
['users', 'tasks', 'analytics']

---

Java Service Setup (Spring Boot)
Add Dependency (pom.xml)

```bash
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-mongodb</artifactId>
</dependency>
```

Update application.properties

```bash
spring.data.mongodb.uri=${MONGO_URI}
```

Set Environment Variable

Mac/Linux:

```bash
export MONGO_URI="mongodb+srv://java_service:password@a5.lyeaaef.mongodb.net/internverse?appName=A5"
```

Windows:

```bash
set MONGO_URI=mongodb+srv://java_service:password@a5.lyeaaef.mongodb.net/internverse?appName=A5
```

Run application.

If it starts without MongoDB connection errors → Success.

# Node.js Service Setup

If using Mongoose:

Install

```bash
npm install mongoose dotenv
```

Setup Connection

```bash
import mongoose from "mongoose";
import dotenv from "dotenv";

dotenv.config();

mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("MongoDB Connected"))
  .catch(err => console.error(err));
```

Service Responsibilities
| Service | Reads | Writes |
| ------- | ------------ | ---------------- |
| Node | users, tasks | users, tasks |
| Python | tasks | analytics |
| Java | analytics | (optional) users |

Timestamps Policy

All collections use:

createdAt
updatedAt

Services must:
Set createdAt when inserting
Update updatedAt on modification
Troubleshooting

If Connection Fails:
Check correct username/password
Confirm internverse database is specified in URI
Ensure .env file is loaded properly
