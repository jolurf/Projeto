from app import app,db 
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from datetime import datetime 

from models import Task
import forms



@app.route('/')
@app.route('/index')
def index():
    tasks = Task.query.all()
    return render_template('index.html', template_folder='./templates', current_title='Custom Title', tasks=tasks)

@app.route('/add', methods=['GET','POST'])
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        t = Task(title=form.title.data, date = datetime.utcnow())
        db.session.add(t) #adiciona o objeto task à base de dados
        db.session.commit() #comita
        # print('Submitted title', form.title.data)
        # return render_template('about.html',form=form, title=form.title.data)
        flash("Task added to the database")
        return redirect(url_for('index')) #redireciona para o index
    return render_template('add.html', form=form)

@app.route('/edit/<int:task_id>', methods=['GET','POST']) #if returns method not allowed pass methods
def edit(task_id):
    task = Task.query.get(task_id) #get the task by id
    form = forms.AddTaskForm()
    if task:
        if form.validate_on_submit():
                task.title = form.title.data
                task.date = datetime.utcnow()
                db.session.commit()
                flash("Task has been updated")
                return redirect(url_for('index'))


        form.title.data = task.title
        return render_template('edit.html', form=form,
        task_id=task_id)
    else:
        flash("Task not found")
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get(task_id) #get the task by id
    form = forms.DeleteTaskForm()
    if task:
        if form.validate_on_submit():
                db.session.delete(task)
                db.session.commit()
                flash("Task has been deleted")
                return redirect(url_for('index'))

        return render_template('delete.html', form=form,
        task_id=task_id, title=task.title)

    else:
        flash("Task not found")
    return redirect(url_for('index'))