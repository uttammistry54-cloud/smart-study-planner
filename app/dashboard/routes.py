from datetime import datetime, timedelta

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models import Exam, Goal, StudySession, Task

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def home():
    today = datetime.utcnow().date()

    # --- Today's goals vs progress ---
    todays_goals = Goal.query.filter_by(user_id=current_user.id, date=today).all()

    goal_progress = []
    for goal in todays_goals:
        session_query = StudySession.query.filter_by(user_id=current_user.id, date=today)
        if goal.subject and goal.subject != "Overall":
            session_query = session_query.filter_by(subject=goal.subject)
        minutes_done = session_query.with_entities(
            func.coalesce(func.sum(StudySession.duration_min), 0)
        ).scalar()

        goal_progress.append(
            {
                "id": goal.id,
                "subject": goal.subject,
                "target_minutes": goal.target_minutes,
                "done_minutes": int(minutes_done),
                "percent": min(100, round((minutes_done / goal.target_minutes) * 100))
                if goal.target_minutes
                else 0,
            }
        )

    # --- Upcoming tasks (next 7 days, not completed) ---
    upcoming_cutoff = today + timedelta(days=7)
    upcoming_tasks = (
        Task.query.filter(
            Task.user_id == current_user.id,
            Task.status == "pending",
            Task.due_date != None,  # noqa: E711
            Task.due_date >= today,
            Task.due_date <= upcoming_cutoff,
        )
        .order_by(Task.due_date.asc())
        .limit(6)
        .all()
    )

    # --- Study statistics ---
    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    completed_tasks = Task.query.filter_by(user_id=current_user.id, status="completed").count()
    completion_rate = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

    week_start = today - timedelta(days=today.weekday())
    week_minutes = (
        db.session.query(func.coalesce(func.sum(StudySession.duration_min), 0))
        .filter(
            StudySession.user_id == current_user.id,
            StudySession.date >= week_start,
            StudySession.date <= today,
        )
        .scalar()
    )

    today_minutes = (
        db.session.query(func.coalesce(func.sum(StudySession.duration_min), 0))
        .filter(StudySession.user_id == current_user.id, StudySession.date == today)
        .scalar()
    )

    # --- Nearest exam countdown ---
    next_exam = (
        Exam.query.filter(Exam.user_id == current_user.id, Exam.exam_date >= today)
        .order_by(Exam.exam_date.asc())
        .first()
    )
    next_exam_data = None
    if next_exam:
        days_left = (next_exam.exam_date - today).days
        next_exam_data = {
            "subject": next_exam.subject,
            "exam_date": next_exam.exam_date.strftime("%d %b %Y"),
            "days_left": days_left,
        }

    stats = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
        "today_minutes": int(today_minutes),
        "week_minutes": int(week_minutes),
        "week_hours": round(week_minutes / 60, 1),
    }

    return render_template(
        "dashboard/index.html",
        goal_progress=goal_progress,
        upcoming_tasks=upcoming_tasks,
        stats=stats,
        next_exam=next_exam_data,
        today=today,
    )


@dashboard_bp.route("/goals", methods=["POST"])
@login_required
def set_goal():
    """Create or update today's study goal (overall or per-subject)."""
    data = request.get_json(silent=True) or request.form
    subject = (data.get("subject") or "Overall").strip()
    try:
        target_minutes = int(data.get("target_minutes", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid target minutes"}), 400

    if target_minutes <= 0:
        return jsonify({"error": "Target must be greater than 0"}), 400

    today = datetime.utcnow().date()
    goal = Goal.query.filter_by(user_id=current_user.id, subject=subject, date=today).first()

    if goal:
        goal.target_minutes = target_minutes
    else:
        goal = Goal(
            user_id=current_user.id, subject=subject, target_minutes=target_minutes, date=today
        )
        db.session.add(goal)

    db.session.commit()
    return jsonify({"success": True, "id": goal.id, "subject": goal.subject,
                     "target_minutes": goal.target_minutes})


@dashboard_bp.route("/goals/<int:goal_id>", methods=["DELETE"])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
    if not goal:
        return jsonify({"error": "Goal not found"}), 404
    db.session.delete(goal)
    db.session.commit()
    return jsonify({"success": True})


@dashboard_bp.route("/log-session", methods=["POST"])
@login_required
def log_session():
    """Quick-log study minutes for a subject today (updates progress bars)."""
    data = request.get_json(silent=True) or request.form
    subject = (data.get("subject") or "").strip()
    try:
        duration_min = int(data.get("duration_min", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid duration"}), 400

    if not subject or duration_min <= 0:
        return jsonify({"error": "Subject and a positive duration are required"}), 400

    session_entry = StudySession(
        user_id=current_user.id,
        subject=subject,
        duration_min=duration_min,
        date=datetime.utcnow().date(),
    )
    db.session.add(session_entry)
    db.session.commit()
    return jsonify({"success": True, "id": session_entry.id})
