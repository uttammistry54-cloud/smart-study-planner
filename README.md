# 📘 Smart Study Planner

A full-stack study planning web application built with **Flask**, **SQLite**, and vanilla **JavaScript**. Helps students set daily study goals, manage tasks, build a weekly timetable, track exam countdowns, and visualize productivity through analytics charts.

## ✨ Features

- **User Authentication** — Register, login, logout (secure password hashing via Werkzeug, session management via Flask-Login)
- **Study Dashboard** — Daily study goals with live progress bars, upcoming tasks, key statistics
- **Task Management** — Full CRUD (add, edit, delete, mark complete) with subject, priority, and due date
- **Study Planner** — Weekly timetable grid (subject-wise scheduling) + exam countdown tracker
- **Productivity Analytics** — Study hours chart, task completion rate, time-by-subject breakdown, weekly progress (powered by Chart.js)
- **Responsive UI** — Mobile-friendly sidebar navigation, modern card-based dashboard design

## 🛠️ Tech Stack

| Layer    | Technology                          |
|----------|--------------------------------------|
| Backend  | Flask, Flask-SQLAlchemy, Flask-Login |
| Database | SQLite                               |
| Frontend | HTML5, CSS3 (custom), Vanilla JS     |
| Charts   | Chart.js (CDN)                       |

## 📁 Project Structure

```
smart-study-planner/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py             # Configuration
│   ├── models.py             # Database models
│   ├── auth/                 # Login/Register/Logout
│   ├── dashboard/            # Dashboard + goals
│   ├── tasks/                 # Task CRUD
│   ├── planner/               # Timetable + exams
│   ├── analytics/             # Chart JSON APIs
│   ├── static/                # CSS, JS, images
│   └── templates/             # Jinja2 HTML templates
├── instance/                  # SQLite DB (auto-created)
├── run.py                     # Entry point
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone & set up a virtual environment

```bash
git clone <your-repo-url>
cd smart-study-planner
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python run.py
```

The app will be available at **http://127.0.0.1:5000**. The SQLite database (`instance/study_planner.db`) is created automatically on first run.

### 4. Create an account

Visit `/auth/register`, sign up, then log in to access the dashboard.

## 🗄️ Database Schema

- **users** — id, name, email, password_hash, created_at
- **tasks** — id, user_id, title, subject, description, due_date, priority, status, created_at
- **study_sessions** — id, user_id, subject, duration_min, date, created_at
- **timetable_entries** — id, user_id, day_of_week, subject, start_time, end_time, created_at
- **exams** — id, user_id, subject, exam_date, created_at
- **goals** — id, user_id, subject, target_minutes, date, created_at

## 📦 Deployment Notes

- Set a strong `SECRET_KEY` environment variable in production.
- For production databases, set `DATABASE_URL` (defaults to local SQLite file).
- Set `debug=False` in `run.py` before deploying.
- Suitable for deployment on Render, Railway, PythonAnywhere, or any WSGI-compatible host (e.g., via Gunicorn: `gunicorn run:app`).

## 📄 License

Built as a portfolio project. Free to use and modify.
