# -*- coding: utf-8 -*-
# app/user/views.py

from flask import render_template, render_template_string, flash, redirect, url_for, request
from flask_login import login_required
from flask_table import Table, Col

from .forms import AddForm, EditForm
from .. import db
from . import user
from ..models import User
from ..views import NoEscapeCol

class UserTable(Table):
    id = Col('Id')
    email = Col('Email')
    username = Col('Username')
    first_name = Col('First name')
    last_name = Col('Last name')
    is_admin = Col('Admin')
    delete = NoEscapeCol('')
    edit = NoEscapeCol('')
    classes = ['table ' 'table-striped ' 'table-bordered ']
    html_attrs = {'id': 'usertable', 'cellspacing': '0', 'width': '100%'}

#show a list of users
@user.route('/user', methods=['GET', 'POST'])
@login_required
def users():
    """
    Handle requests to the /user route
    List the users
    """
    users = User.query.all()
    for u in users:
        u.delete = render_template_string("<a class='confirmBeforeDelete' u_id=" + str(u.id) + "><i class='fa fa-trash'></i></a>")
        u.edit = render_template_string("<a href=\"{{ url_for('user.edit', id=" + str(u.id) + ") }}\"><i class='fa fa-pencil'></i>")
    user_table = UserTable(users)

    return render_template('user/users.html', title='Users', route='user.users', subject='user', table=user_table)


#add a new user
@user.route('/user/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                        username=form.username.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have added user {}'.format(user.username))

        return redirect(url_for('user.users'))

    return render_template('user/user.html', form=form, title='Add')


#edit a user
@user.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get_or_404(id)
    form = EditForm(obj=user)
    if form.validate_on_submit():
        if request.form['button'] == 'Save':
            form.populate_obj(user)
            db.session.commit()
            flash('You have edited user {}'.format(user.username))

        return redirect(url_for('user.users'))

    return render_template('user/user.html', form=form, title='Edit')


#delete a user
@user.route('/user/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    return redirect(url_for('user.users'))

