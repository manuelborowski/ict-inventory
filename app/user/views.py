# -*- coding: utf-8 -*-
# app/user/views.py

from flask import render_template, render_template_string, flash, redirect, url_for
from flask_login import login_required
from flask_table import Table, Col

from .forms import UserForm
from .. import db
from . import user
from ..models import User


#Special column to add html-tags.  Note : this can be dangerous, so whatch out!!!
class NoEscapeCol(Col):
    def td_format(self, content):
        return content

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
        u.delete = render_template_string("<a href=\"{{ url_for('user.delete', id=" + str(u.id) + ") }}\"><i class='fa fa-trash'></i>")
        u.edit = render_template_string("<a href=\"{{ url_for('user.edit', id=" + str(u.id) + ") }}\"><i class='fa fa-pencil'></i>")
    user_table = UserTable(users)

    return render_template('user/user.html', title='Users', user_table=user_table, table_id='usertable')


#add a new user
@user.route('/user/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Handle requests to the /user/add route
    Add a new user
    """

    form = UserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                        username=form.username.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        password=form.password.data)

        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash('You have added user {}'.format(form.username.data))

        # redirect to the user page
        return redirect(url_for('user.users'))

    # load registration template
    return render_template('user/register.html', form=form, title='Register')


#delete a user
@user.route('/user/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    print('delete user with id {}'.format(id))

    return redirect(url_for('user.users'))

#edit a user
@user.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    print('edit user with id {}'.format(id))

    return redirect(url_for('user.users'))