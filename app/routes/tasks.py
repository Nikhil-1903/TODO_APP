from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.models import Task

tasks_bp  = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def home():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)


@tasks_bp.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')

    if not title:
        flash('task  title cannot be empty')
        return redirect(url_for('tasks.home'))

    # TEMP: assigning task to user with id=1
    # This will be replaced by current_user.id later
    task = Task(title=title, user_id=current_user.id)

    db.session.add(task)
    db.session.commit()

    flash('Task added successfully')
    return redirect(url_for('tasks.home'))


@tasks_bp.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = "Completed"

    db.session.commit()
    flash("task marked as completed.")
    return redirect(url_for('tasks.home'))


@tasks_bp.ropute('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.queryget_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    flash("task deleted")
    return redirect(url_for('tasks.home'))