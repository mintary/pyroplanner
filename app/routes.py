from flask import redirect, render_template, url_for, request, session, flash
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app import db
from .forms import LoginForm, CreateAccountForm, TaskForm
from app.models import User, Task

import sqlalchemy as sa
import string
import random
from datetime import datetime, timedelta

@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('dashboard'))

    return render_template('login.html', title="Login", form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create_account', methods=('GET', 'POST'))
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Account created!')

        return redirect(url_for('login'))

    return render_template('create_account.html', title='Create Account', form=form)

@login_required
@app.route('/dashboard')
def dashboard():
    u = current_user
    query = u.tasks.select()
    tasks = db.session.scalars(query).all()

    date_now = datetime.now()
    format_str = '%D:%M:%Y'

    incomplete_weight_sum = 0
    task_sum = 0
    seconds_left = 0
    total_seconds = 0

    for task in tasks:
        task_sum += task.weight_user
        total_seconds += (task.deadline - task.timestamp).total_seconds()
        if task.complete == False:
            incomplete_weight_sum += task.weight_user
            seconds_left += (task.deadline - date_now).total_seconds()

    print(incomplete_weight_sum)

    passed_info = [incomplete_weight_sum]

    return render_template('dashboard.html', title="Dashboard", tasks=tasks, seconds_left=seconds_left, total_seconds=total_seconds)

@login_required
@app.route('/add_task', methods = ["POST", "GET"])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, deadline=form.deadline.data, weight_user=form.weight_user.data, author=current_user)
        db.session.add(task)
        db.session.commit()

        flash('Task added.')

        return redirect('/dashboard')
    
    return render_template("add_tasks.html", title="Add a task", form=form)

@login_required
@app.route("/update/<int:task_id>")
def update(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        task.complete = not task.complete
        db.session.commit()
    return redirect(url_for("dashboard"))

@login_required
@app.route("/delete/<int:task_id>", methods=["GET", "POST"])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()

    db.session.delete(task)
    db.session.commit()

    flash("Task has been deleted.")

    return redirect(url_for("dashboard"))