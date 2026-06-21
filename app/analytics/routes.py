from datetime import datetime, timedelta

from flask import Blueprint, jsonify, render_template
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models import StudySession, Task

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/")
@login_required
def index():
    return render_template("analytics/index.html")


@analytics_bp.route("/api/weekly-hours")
@login_required
def weekly_hours():
    """Study minutes per day for the last 7 days (for bar/line chart)."""
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=6)

    rows = (
        db.session.query(
            StudySession.date, func.sum(StudySession.duration_min).label("total")
        )
        .filter(
            StudySession.user_id == current_user.id,
            StudySession.date >= start_date,
            StudySession.date <= today,
        )
        .group_by(StudySession.date)
        .all()
    )
    totals_by_date = {row.date: row.total for row in rows}

    labels = []
    minutes = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        labels.append(day.strftime("%a"))
        minutes.append(int(totals_by_date.get(day, 0)))

    return jsonify({"labels": labels, "minutes": minutes, "hours": [round(m / 60, 2) for m in minutes]})


@analytics_bp.route("/api/subject-breakdown")
@login_required
def subject_breakdown():
    """Total study minutes grouped by subject (for pie/doughnut chart)."""
    rows = (
        db.session.query(
            StudySession.subject, func.sum(StudySession.duration_min).label("total")
        )
        .filter(StudySession.user_id == current_user.id)
        .group_by(StudySession.subject)
        .order_by(func.sum(StudySession.duration_min).desc())
        .all()
    )

    return jsonify(
        {
            "labels": [row.subject for row in rows],
            "minutes": [int(row.total) for row in rows],
        }
    )


@analytics_bp.route("/api/completion-rate")
@login_required
def completion_rate():
    total = Task.query.filter_by(user_id=current_user.id).count()
    completed = Task.query.filter_by(user_id=current_user.id, status="completed").count()
    pending = total - completed
    rate = round((completed / total) * 100) if total else 0

    return jsonify(
        {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": rate,
        }
    )


@analytics_bp.route("/api/weekly-progress")
@login_required
def weekly_progress():
    """Tasks completed per day over the last 7 days (for line chart)."""
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=6)

    rows = (
        db.session.query(
            func.date(Task.created_at).label("day"), func.count(Task.id).label("total")
        )
        .filter(
            Task.user_id == current_user.id,
            Task.status == "completed",
            func.date(Task.created_at) >= start_date.isoformat(),
        )
        .group_by("day")
        .all()
    )
    totals_by_date = {row.day: row.total for row in rows}

    labels = []
    counts = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        labels.append(day.strftime("%a"))
        counts.append(int(totals_by_date.get(day.isoformat(), 0)))

    return jsonify({"labels": labels, "completed_counts": counts})
