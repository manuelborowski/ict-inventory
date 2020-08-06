from flask import render_template, redirect, url_for, request
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from app import db, log, admin_required, user_plus_required
from . import category
from app.models import DeviceCategory

from app.support import build_filter, get_ajax_table
from app.tables_config import  tables_configuration

@category.route('/management/device_category/data', methods=['GET', 'POST'])
@login_required
@user_plus_required
def source_data():
    return get_ajax_table(tables_configuration['device_category'])

@category.route('/management/device_category', methods=['GET', 'POST'])
@login_required
@user_plus_required
def show():
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['device_category'])
    config = tables_configuration['device_category']
    return render_template('base_multiple_items.html',
                           title='device_categories',
                           filter=_filter, filter_form=_filter_form,
                           config=config)


@category.route('/management/device_category/add/<int:id>', methods=['GET', 'POST'])
@category.route('/management/device_category/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add(id=-1):
    if id > -1:
        category = DeviceCategory.query.get_or_404(int(id))
        form = AddForm(obj=category)
    else:
        form = AddForm()
        form.active.data = True
    del form.id # is not required here and makes validate_on_submit fail...
    #Validate on the second pass only (when button 'Bewaar' is pushed)
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        category = DeviceCategory(name=form.name.data,
                                  active=form.active.data,
                                  info=form.info.data)
        db.session.add(category)
        db.session.commit()
        log.info(f'add : {category}')
        return redirect(url_for('management.device_category.show'))
    return render_template('management/device_category/category.html', form=form, title='Add a category', role='add', subject='management.device_category')


@category.route('/management/device_category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = DeviceCategory.query.get_or_404(id)
    form = EditForm(obj=category)
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(category)
            db.session.commit()
        return redirect(url_for('management.device_category.show'))
    return render_template('management/device_category/category.html', form=form, title='Edit a category', role='edit', subject='management.device_category')


@category.route('/management/device_category/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    category = DeviceCategory.query.get_or_404(id)
    form = ViewForm(obj=category)
    if form.validate_on_submit():
        return redirect(url_for('management.device_category.show'))
    return render_template('management/device_category/category.html', form=form, title='View a category', role='view', subject='management.device_category')