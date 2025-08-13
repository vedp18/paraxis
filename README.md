# PARAXIS — Django Social Platform

A social web application built with **Django**, featuring:
- User authentication and profiles
- Image-based posts
- Real-time **views tracking** via **Redis**
- Secure development with **HTTPS** support

---

## Introduction
**ParaXis** is a social platform where users can:
- Sign up and log in
- Create posts with images
- Track engagement metrics like views and likes in real-time using Redis

It’s designed as both a **Django learning project** and a starting point for building more complex social platforms.

---

## Project Structure

```

paraxis/
├── account/          # Authentication, profiles, user views
├── post/             # Post creation, listing, detail views, like/view logic
├── media/            # Uploaded images storage
├── paraxis/          # Django project settings and URL configuration
├── manage.py         # Django management tool
├── requirement.txt   # Project dependencies
├── cert.crt          # Self-signed SSL certificate (dev only - will be generated when running https developement server)
├── cert.key          # SSL key (dev only - will be generated when running https developement server)
├── secret_keys.py    # Secret keys & sensitive variables (excluded from VCS)
└── db.sqlite3        # SQLite database (dev only - will be generated when you migrate models to database using ```python manage.py migrate```)

````

---

## Features
- **User Authentication** — Registration, login, logout, profiles
- **Image Posts** — Create and display posts with images
- **User Views Tracking** — Using Redis for fast metrics
- **Persistent Redis Storage** — Docker volume for metric persistence
- **HTTPS Dev Server** — Self-signed SSL cert for local testing

---

## Tech Stack
- **Backend:** Django 3.x+
- **Database:** SQLite (dev), can switch to PostgreSQL/MySQL
- **Cache / Metrics:** Redis (via Docker)
- **Frontend:** Django templates, Html
- **Environment:** Python 3.8+, Docker

---

## Installation

### Prerequisites
- Python 3.8+
- Docker (for Redis)
- OpenSSL (for generating SSL certs)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/vedp18/paraxis.git
cd paraxis

# 2. Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirement.txt

# 3. Start Redis with Docker
docker pull redis
docker volume create redis_data
docker run -d --name paraxis-redis -p 6379:6379 \
  -v redis_data:/data \
  redis redis-server --appendonly yes

# 4. Apply migrations
python manage.py migrate

# 5. (Optional) Create admin user
python manage.py createsuperuser

# 6. Run server
# HTTPS (recommended for social logins):
python manage.py runserver_plus --cert-file cert.crt
# or HTTP:
python manage.py runserver
````

---

## Configuration

* **`secret_keys.py`** — Stores `SOCIAL SECRET_KEYS` for Authentication
* **Redis Connection** — Update in `settings.py` if using external/production Redis

---

## Usage

1. Start Redis and Django server
2. Open `https://127.0.0.1:8000` or `https://paraxis.com:8000` in your browser
3. Register or log in
4. Create posts with images
5. View counts and likes update in real-time via Redis

---

## Workflow

1. **User signs up/logs in**
2. **Posts an image**
3. Each post views updates Redis with key:

   ```
   post:<id>:viewers
   ```
4. Profile page dynamically shows `.total_views` from Redis
5. Metrics persist via Docker volumes

---

## Useful Commands

| Task               | Command                                                |
| ------------------ | ------------------------------------------------------ |
| Apply migrations   | `python manage.py migrate`                             |
| Create superuser   | `python manage.py createsuperuser`                     |
| Run server (HTTPS) | `python manage.py runserver_plus --cert-file cert.crt` |
| Start Redis        | `docker start paraxis-redis`                           |
| Stop Redis         | `docker stop paraxis-redis`                            |

---

## Troubleshooting

* **Redis connection error:** Ensure the Docker container is running and port `6379` is free.
* **SSL errors in dev:** Use `--cert-file cert.crt` only if `cert.key` is present; otherwise regenerate using OpenSSL:

  ```bash
  openssl req -x509 -newkey rsa:4096 -keyout cert.key -out cert.crt -days 365 -nodes
  ```
* **Metrics not updating:** Confirm Redis volume `redis_data` is intact and mapped correctly.


---
