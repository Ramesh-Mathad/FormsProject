# FormsProject — Student Management System

> **Cloud & DevOps Internship Assignment | AWS + Docker Deployment**

[![Live Application](https://img.shields.io/badge/Live%20Application-HTTPS-success)](https://formsproject-ramesh.duckdns.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)](https://www.docker.com/)
[![AWS EC2](https://img.shields.io/badge/AWS-EC2-orange)](https://aws.amazon.com/ec2/)

## 🔗 Project Links

| Resource | Link |
|---|---|
| **Live Application** | https://formsproject-ramesh.duckdns.org/ |
| **GitHub Repository** | https://github.com/Ramesh-Mathad/FormsProject |

---

## 1. Project Overview

**FormsProject** is a Django-based Student Management System / Campus Portal.

The application provides a simple interface to manage student records and supports:

- Create student records
- View student records
- Update student records
- Delete student records
- Upload and display student images

The application is containerized with **Docker** and deployed on **AWS EC2**. It is publicly accessible through a **DuckDNS domain** with **HTTPS** enabled through Nginx and Let's Encrypt.

---

## 2. Project Objective

The main objective of this project is to demonstrate the deployment of a simple Docker application on AWS and make it accessible through the internet.

The implementation demonstrates:

- Docker containerization
- AWS EC2 deployment
- DNS configuration
- HTTPS/TLS
- Reverse proxy configuration
- AWS Security Groups
- Persistent application data
- Basic deployment security
- Troubleshooting and problem solving

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Application programming language |
| **Django** | Web application framework |
| **SQLite** | Application database |
| **Pillow** | Image processing/upload support |
| **Docker** | Application containerization |
| **AWS EC2** | Cloud hosting |
| **Nginx** | Reverse proxy, HTTPS and static/media serving |
| **DuckDNS** | DNS/domain |
| **Let's Encrypt** | TLS/HTTPS certificate |
| **GitHub** | Source code management |

---

## 4. Architecture

```text
                         ┌─────────────────────┐
                         │   User / Internet   │
                         └──────────┬──────────┘
                                    │
                              HTTPS / 443
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      DuckDNS        │
                         │ formsproject-       │
                         │ ramesh.duckdns.org  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                 ┌──────────────────────────────────┐
                 │          AWS EC2 Instance         │
                 │                                  │
                 │  ┌────────────────────────────┐  │
                 │  │     Security Group         │  │
                 │  │  SSH 22 - restricted       │  │
                 │  │  HTTP 80                    │  │
                 │  │  HTTPS 443                  │  │
                 │  └─────────────┬──────────────┘  │
                 │                │                 │
                 │                ▼                 │
                 │  ┌────────────────────────────┐  │
                 │  │          Nginx             │  │
                 │  │  TLS + Reverse Proxy       │  │
                 │  └─────────────┬──────────────┘  │
                 │                │                 │
                 │                ▼                 │
                 │  ┌────────────────────────────┐  │
                 │  │     Docker Container       │  │
                 │  │       Django App           │  │
                 │  └─────────────┬──────────────┘  │
                 │                │                 │
                 │        ┌───────┴────────┐        │
                 │        ▼                ▼        │
                 │   ┌─────────┐      ┌─────────┐  │
                 │   │ SQLite  │      │  Media  │  │
                 │   │   DB    │      │ Uploads │  │
                 │   └─────────┘      └─────────┘  │
                 └──────────────────────────────────┘
```

### Request Flow

**Browser → DuckDNS → AWS EC2 → Security Group → Nginx → Docker → Django → SQLite**

Static files and uploaded media are served through Nginx.

---

## 5. Why These Services Were Selected

### AWS EC2

**What:** A virtual Linux server hosted by AWS.

**Why:** EC2 provides direct control of the server, making it simple to install Docker and Nginx and understand the deployment process.

**Alternative:** ECS/Fargate would provide a more managed container platform, but it introduces additional AWS configuration that is unnecessary for this small application.

### Docker

**What:** A containerization platform.

**Why:** Docker packages the application and its dependencies together, making deployment consistent between environments.

### Security Group

**What:** AWS network-level firewall for the EC2 instance.

**Why:** It controls which traffic can reach the server.

The final configuration allows:
- SSH only from the required restricted sources
- HTTP on port 80
- HTTPS on port 443

Public access to port **8000 was removed** because users should access the application through Nginx/HTTPS.

### Nginx

**What:** Web server and reverse proxy.

**Why:** Nginx provides HTTPS termination, forwards application requests to Django, and serves static and media files efficiently.

### DuckDNS

**What:** Free DNS service providing a hostname.

**Why:** It provides a usable domain for the AWS-hosted application without requiring a paid domain.

### Let's Encrypt

**What:** Certificate Authority providing TLS certificates.

**Why:** It provides HTTPS for the public application.

### SQLite

**What:** Lightweight relational database.

**Why:** The application is a small CRUD project, so a separate database server is unnecessary for the assignment.

**Alternative:** Amazon RDS with PostgreSQL/MySQL would be more appropriate for a larger production application.

---

## 6. Docker Configuration

The application uses a Python 3.12 slim Docker image.

### Build the image

```bash
docker build -t formsproject .
```

### Run the container

```bash
docker run -d -p 8000:8000 \
  --name formsproject-container \
  -v ~/FormsProject/db.sqlite3:/app/db.sqlite3 \
  -v ~/FormsProject/media:/app/media \
  -e DJANGO_SECRET_KEY="YOUR_SECRET_KEY" \
  -e DJANGO_DEBUG=False \
  -e DJANGO_ALLOWED_HOSTS="YOUR_HOSTS" \
  -e DJANGO_CSRF_TRUSTED_ORIGINS="https://formsproject-ramesh.duckdns.org" \
  formsproject
```

> **Security:** Real secret values must never be committed to GitHub.

---

## 7. Database and Media Persistence

A Docker container can be recreated or replaced, so application data should not exist only inside the container.

For this reason, persistent host directories are mounted:

```text
EC2 host                         Docker container

~/FormsProject/db.sqlite3  ───►  /app/db.sqlite3

~/FormsProject/media       ───►  /app/media
```

This keeps:

- Student database records
- Uploaded student images

available even when the Docker container is recreated.

---

## 8. Static Files

The application runs with:

```text
DEBUG=False
```

Django static files are collected using:

```bash
docker exec formsproject-container python manage.py collectstatic --noinput
```

Nginx serves the collected `/static/` files directly.

This allows the application to retain production-style Django security settings while keeping the original UI working correctly.

---

## 9. HTTPS and DNS

The application is available at:

**https://formsproject-ramesh.duckdns.org/**

The deployment uses:

```text
HTTP :80
   │
   ▼
HTTPS :443
   │
   ▼
Nginx
   │
   ▼
Docker :8000
   │
   ▼
Django
```

Nginx uses the Let's Encrypt certificate and redirects HTTP traffic to HTTPS.

---

## 10. Security Implementation

The final deployment includes:

- `DEBUG=False`
- Strong random Django secret supplied through an environment variable
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- Secure session cookies
- Secure CSRF cookies
- HTTPS redirect
- HSTS
- Nginx TLS termination
- Restricted SSH access
- Port 8000 removed from public Security Group access
- Secrets excluded from GitHub
- Persistent application data stored outside the container

---

## 11. Deployment Process

The deployment was completed using the following process:

```text
1. Prepared Django application
        ↓
2. Added Dockerfile and requirements
        ↓
3. Built and tested Docker image locally
        ↓
4. Created AWS EC2 instance
        ↓
5. Installed Docker on EC2
        ↓
6. Cloned project from GitHub
        ↓
7. Built and started Docker container
        ↓
8. Configured database and media persistence
        ↓
9. Configured AWS Security Group
        ↓
10. Configured DuckDNS
        ↓
11. Installed and configured Nginx
        ↓
12. Enabled HTTPS with Let's Encrypt
        ↓
13. Configured Django host/CSRF/security settings
        ↓
14. Configured static and media serving
        ↓
15. Tested the complete application
```

---

## 12. Problems Encountered and Solutions

### Problem 1 — Django `DisallowedHost`

**Issue:** Django rejected requests made using the EC2 IP/domain.

**Solution:** Configured `DJANGO_ALLOWED_HOSTS` with the required IP addresses and domain.

---

### Problem 2 — CSRF verification failed

**Issue:** HTTPS POST requests returned an origin-checking error.

**Solution:** Added:

```text
https://formsproject-ramesh.duckdns.org
```

to Django's `CSRF_TRUSTED_ORIGINS`.

---

### Problem 3 — HTTPS initially timed out

**Issue:** The application was reachable but HTTPS traffic could not reach the EC2 instance.

**Solution:** Added inbound HTTPS port 443 to the AWS Security Group and configured Nginx with the Let's Encrypt certificate.

---

### Problem 4 — UI lost its CSS after `DEBUG=False`

**Issue:** The HTML loaded but the original styling disappeared.

**Cause:** Django's development static-file serving is not intended for this deployment configuration.

**Solution:** Ran `collectstatic` and configured Nginx to serve `/static/`.

---

### Problem 5 — Uploaded images returned permission errors

**Issue:** Nginx could not read uploaded media files.

**Solution:** Corrected filesystem access and configured Nginx to serve `/media/`.

---

### Problem 6 — Database persistence

**Issue:** Recreating a container could remove database data stored only inside the container.

**Solution:** Mounted `db.sqlite3` from the EC2 host into the Docker container.

---

### Problem 7 — Uploaded media persistence

**Issue:** Uploaded images could be lost when the container was recreated.

**Solution:** Mounted the EC2 `media` directory into the Docker container.

---

## 13. Testing and Verification

The final deployment was tested through the public HTTPS domain.

### Application tests

- [x] Application loads
- [x] HTTPS works
- [x] Student records display
- [x] Student can be added
- [x] Student image can be uploaded
- [x] Uploaded image displays correctly
- [x] Student can be updated
- [x] Student can be deleted
- [x] Database data persists
- [x] Media files persist

### Django verification

```bash
docker exec formsproject-container python manage.py check
```

Result:

```text
System check identified no issues (0 silenced).
```

### Docker verification

```bash
docker ps
```

The `formsproject-container` was confirmed running successfully.

---

## 14. Repository Structure

```text
FormsProject/
│
├── FormsProject/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── student/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── templates/
├── static/
├── media/
├── Dockerfile
├── requirements.txt
├── .gitignore
├── .dockerignore
└── manage.py
```

---

## 15. Known Limitation and Future Improvements

This deployment intentionally uses a simple architecture appropriate for the assignment.

For a larger production system, it could be improved with:

- **Amazon RDS** → managed PostgreSQL/MySQL
- **Amazon S3** → persistent object storage for uploaded media
- **ECS/Fargate** → managed container deployment
- **Application Load Balancer** → scalable traffic distribution
- **CloudFront** → CDN and edge delivery
- **CloudWatch** → monitoring and centralized logs
- **Elastic IP** → stable EC2 public IP

These services were not added because they would increase complexity without being necessary for the current project scope.

---

## 16. Conclusion

FormsProject demonstrates a complete path from a Django application to a publicly accessible cloud deployment.

The final architecture is:

> **DuckDNS → AWS EC2 → Security Group → Nginx/HTTPS → Docker → Django → SQLite**

The project demonstrates practical understanding of:

**Docker + AWS + DNS + HTTPS + Linux + Reverse Proxy + Persistence + Security + Troubleshooting**

The deployment is intentionally simple, understandable and reproducible while meeting the requirements of the assignment.
