from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def _parse_due_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


@tasks_bp.route("/")
@login_required
def index():
    filter_status = request.args.get("status", "all")
    query = Task.query.filter_by(user_id=current_user.id)

    if filter_status == "pending":
        query = query.filter_by(status="pending")
    elif filter_status == "completed":
        query = query.filter_by(status="completed")

    all_tasks = query.order_by(
        Task.status.asc(), Task.due_date.is_(None), Task.due_date.asc()
    ).all()

    return render_template("tasks/index.html", tasks=all_tasks, filter_status=filter_status)


@tasks_bp.route("/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    description = request.form.get("description", "").strip()
    due_date = _parse_due_date(request.form.get("due_date", ""))
    priority = request.form.get("priority", "medium")

    if priority not in ("low", "medium", "high"):
        priority = "medium"

    if not title:
        flash("Task title is required.", "error")
        return redirect(url_for("tasks.index"))

    task = Task(
        user_id=current_user.id,
        title=title,
        subject=subject or None,
        description=description or None,
        due_date=due_date,
        priority=priority,
        status="pending",
    )
    db.session.add(task)
    db.session.commit()
    flash("Task added successfully.", "success")
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/edit/<int:task_id>", methods=["POST"])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("tasks.index"))

    title = request.form.get("title", "").strip()
    if not title:
        flash("Task title is required.", "error")
        return redirect(url_for("tasks.index"))

    task.title = title
    task.subject = request.form.get("subject", "").strip() or None
    task.description = request.form.get("description", "").strip() or None
    task.due_date = _parse_due_date(request.form.get("due_date", ""))
    priority = request.form.get("priority", "medium")
    task.priority = priority if priority in ("low", "medium", "high") else "medium"

    db.session.commit()
    flash("Task updated successfully.", "success")
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("tasks.index"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/toggle/<int:task_id>", methods=["POST"])
@login_required
def toggle_task(task_id):
    """Toggle completion status. Returns JSON for AJAX use, falls back to redirect."""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        if request.is_json or request.accept_mimetypes.accept_json:
            return jsonify({"error": "Task not found"}), 404
        flash("Task not found.", "error")
        return redirect(url_for("tasks.index"))

    task.status = "completed" if task.status == "pending" else "pending"
    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": True, "status": task.status})

    return redirect(url_for("tasks.index"))
