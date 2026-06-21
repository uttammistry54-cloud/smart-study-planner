from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Exam, TimetableEntry

planner_bp = Blueprint("planner", __name__, url_prefix="/planner")

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@planner_bp.route("/")
@login_required
def index():
    entries = TimetableEntry.query.filter_by(user_id=current_user.id).all()

    # Organize entries by day for the weekly grid
    timetable = {day: [] for day in DAYS_OF_WEEK}
    for entry in entries:
        if entry.day_of_week in timetable:
            timetable[entry.day_of_week].append(entry)

    for day in timetable:
        timetable[day].sort(key=lambda e: e.start_time)

    today = datetime.utcnow().date()
    exams = (
        Exam.query.filter_by(user_id=current_user.id)
        .order_by(Exam.exam_date.asc())
        .all()
    )

    exams_with_countdown = []
    for exam in exams:
        days_left = (exam.exam_date - today).days
        exams_with_countdown.append({"exam": exam, "days_left": days_left})

    return render_template(
        "planner/index.html",
        timetable=timetable,
        days_of_week=DAYS_OF_WEEK,
        exams=exams_with_countdown,
    )


@planner_bp.route("/timetable/add", methods=["POST"])
@login_required
def add_timetable_entry():
    day_of_week = request.form.get("day_of_week", "")
    subject = request.form.get("subject", "").strip()
    start_time = request.form.get("start_time", "")
    end_time = request.form.get("end_time", "")

    if day_of_week not in DAYS_OF_WEEK or not subject or not start_time or not end_time:
        flash("All timetable fields are required.", "error")
        return redirect(url_for("planner.index"))

    if start_time >= end_time:
        flash("Start time must be before end time.", "error")
        return redirect(url_for("planner.index"))

    entry = TimetableEntry(
        user_id=current_user.id,
        day_of_week=day_of_week,
        subject=subject,
        start_time=start_time,
        end_time=end_time,
    )
    db.session.add(entry)
    db.session.commit()
    flash("Timetable slot added.", "success")
    return redirect(url_for("planner.index"))


@planner_bp.route("/timetable/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_timetable_entry(entry_id):
    entry = TimetableEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if not entry:
        flash("Timetable entry not found.", "error")
        return redirect(url_for("planner.index"))

    db.session.delete(entry)
    db.session.commit()
    flash("Timetable slot removed.", "info")
    return redirect(url_for("planner.index"))


@planner_bp.route("/exams/add", methods=["POST"])
@login_required
def add_exam():
    subject = request.form.get("subject", "").strip()
    exam_date_str = request.form.get("exam_date", "")

    if not subject or not exam_date_str:
        flash("Subject and exam date are required.", "error")
        return redirect(url_for("planner.index"))

    try:
        exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid exam date.", "error")
        return redirect(url_for("planner.index"))

    exam = Exam(user_id=current_user.id, subject=subject, exam_date=exam_date)
    db.session.add(exam)
    db.session.commit()
    flash("Exam added to countdown.", "success")
    return redirect(url_for("planner.index"))


@planner_bp.route("/exams/delete/<int:exam_id>", methods=["POST"])
@login_required
def delete_exam(exam_id):
    exam = Exam.query.filter_by(id=exam_id, user_id=current_user.id).first()
    if not exam:
        flash("Exam not found.", "error")
        return redirect(url_for("planner.index"))

    db.session.delete(exam)
    db.session.commit()
    flash("Exam removed.", "info")
    return redirect(url_for("planner.index"))
