from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from tasks import Task

tasks_bp = Blueprint('tasks', __name__)                                                                     

@tasks_bp.route('/')
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form.get('title')
    if title:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    else:
        flash('Task title cannot be empty.', 'error')
    
    return redirect(url_for('tasks.view_tasks'))

