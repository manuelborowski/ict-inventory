# -*- coding: utf-8 -*-
# app/user/views.py

from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from flask_table import Table, Col

from .forms import RegistrationForm
from .. import db
from . import user
from ..models import User


class UserTable(Table):
    id = Col('Id')
    email = Col('Email')
    username = Col('Username')
    first_name = Col('First name')
    last_name = Col('Last name')
    is_admin = Col('Admin')
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

    form = RegistrationForm()
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
