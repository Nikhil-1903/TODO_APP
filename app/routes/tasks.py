from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models import Task
from app.forms import TaskForm


tasks_bp  = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def home():
    form = TaskForm()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks, form = form)


@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():

        task = Task(title=form.title.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully')
    return redirect(url_for('tasks.home'))


@tasks_bp.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = "Completed"

    db.session.commit()
    flash("task marked as completed.")
    return redirect(url_for('tasks.home'))


@tasks_bp.ropute('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.queryget_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    flash("task deleted")
    return redirect(url_for('tasks.home'))


@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Ownership check
    if task.user_id != current_user.id:
        flash('Unauthorized action')
        return redirect(url_for('tasks.home'))

    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        db.session.commit()
        flash('Task updated')
        return redirect(url_for('tasks.home'))

    return render_template('edit_task.html', form=form)
