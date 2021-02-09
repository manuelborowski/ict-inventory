# -*- coding: utf-8 -*-
# app/user/views.py

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from .forms import AddForm, EditForm, ViewForm, ChangePasswordForm
from app import db, log, admin_required
from . import user
from app.models import User

from app.support import build_filter, get_ajax_table
from app.tables_config import  tables_configuration

@user.route('/management/user/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['user'])

@user.route('/management/user', methods=['GET', 'POST'])
@login_required
def users():
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['user'])
    config = tables_configuration['user']
    return render_template('base_multiple_items.html', title='users',
                           filter=_filter, filter_form=_filter_form, config=config)


#add a new user
@user.route('/management/user/add/<int:id>', methods=['GET', 'POST'])
@user.route('/management/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add(id=-1):
    if id > -1:
        user = User.query.get_or_404(int(id))
        form = AddForm(obj=user)
    else:
        form = AddForm()
    #Validate on the second pass only (when button 'Bewaar' is pushed)
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data,
                    level=form.level.data,
                )
        db.session.add(user)
        db.session.commit()
        log.info('add : {}'.format(user.log()))
        #flash('You have added user {}'.format(user.username))
        return redirect(url_for('management.user.users'))
    return render_template('management/user/user.html', form=form, title='Add a user', role='add', subject='management.user')


#edit a user
@user.route('/management/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get_or_404(id)
    form = EditForm(obj=user)
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(user)
            db.session.commit()
            #flash('You have edited user {}'.format(user.username))

        return redirect(url_for('management.user.users'))
    return render_template('management/user/user.html', form=form, title='Edit a user', role='edit', subject='management.user')

#no login required
@user.route('/management/user/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    user = User.query.get_or_404(id)
    form = ViewForm(obj=user)
    form.level.data = User.LEVEL.i2s(user.level)
    if form.validate_on_submit():
        return redirect(url_for('management.user.users'))
    return render_template('management/user/user.html', form=form, title='View a user', role='view', subject='management.user')

#delete a user
@user.route('/management/user/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    #flash('You have successfully deleted the user.')
    return redirect(url_for('management.user.users'))

@user.route('/management/user/change-password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id):
    user = User.query.get_or_404(id)
    form = ChangePasswordForm(obj=user)
    if form.validate_on_submit():
        if user.verify_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.commit()
            flash('Your password was successfully changed.')
            return redirect(url_for('management.user.users'))
        flash('Invalid username or password.')
    return render_template('management/user/user.html', form=form, title='Change password', role='change_password', subject='management.user')