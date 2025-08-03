
# Bug Tracker with Real-Time Notifications & Typing Indicator

## Overview

This project provides real-time notifications and typing indicators in a bug tracking system using Django Channels and WebSockets. Users connect to WebSocket endpoints per project and receive live updates about bugs and comments.

---

## WebSocket URL

```
ws://localhost:8000/ws/bugs/<project_id>/?user_id=<user_id>
```

- `project_id` — the ID of the project to join
- `user_id` — the ID of the user connecting

---

## Backend Features

- Real-time bug creation, assignment, updates, and closure notifications.
- Real-time comment notifications.
- Typing indicators for users typing comments in a project.
- Permission checks: only project owners, assigned users, or commenters can connect.

---

## How to Run the Project

### Prerequisites

- Python 3.10+
- Redis server (default on `localhost:6379`)
- PostgreSQL or SQLite configured in Django settings
- Node.js (optional for frontend)

### Setup Steps

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. **Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate    # Windows PowerShell
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root with:

```
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://127.0.0.1:6379
```

5. **Apply migrations**

```bash
python manage.py migrate
```

6. **Create superuser (optional)**

```bash
python manage.py createsuperuser
```

7. **Start Redis**

```bash
redis-server
```

8. **Run the Django application with Uvicorn**

```bash
uvicorn your_project_name.asgi:application --reload
```

Replace `your_project_name` with your actual Django project folder.

9. **Open frontend**

Open the provided `frontend.html` file in a browser to connect and test.

---

## Frontend Sample

A sample HTML frontend is provided to connect via WebSocket, send typing events, and receive bug and comment notifications.

---

## Contact

For questions or contributions, please open an issue or pull request.

---
