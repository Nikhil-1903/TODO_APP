from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. Please login.')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form = form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        



        if not user or not check_password_hash(user.password, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('Logged in successfully')
        return redirect(url_for('tasks.home'))

    return render_template('login.html', form = form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('auth.login'))
