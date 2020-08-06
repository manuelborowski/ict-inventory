from flask import render_template, redirect, url_for, request
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from app import db, log, admin_required, user_plus_required
from . import location
from app.models import AssetLocation

from app.support import build_filter, get_ajax_table
from app.tables_config import  tables_configuration

@location.route('/management/asset_location/data', methods=['GET', 'POST'])
@login_required
@user_plus_required
def source_data():
    return get_ajax_table(tables_configuration['asset_location'])

@location.route('/management/asset_location', methods=['GET', 'POST'])
@login_required
@user_plus_required
def show():
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['asset_location'])
    config = tables_configuration['asset_location']
    return render_template('base_multiple_items.html',
                           title='device_categories',
                           filter=_filter, filter_form=_filter_form,
                           config=config)


@location.route('/management/asset_location/add/<int:id>', methods=['GET', 'POST'])
@location.route('/management/asset_location/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add(id=-1):
    if id > -1:
        location = AssetLocation.query.get_or_404(int(id))
        form = AddForm(obj=location)
    else:
        form = AddForm()
        form.active.data = True
    del form.id # is not required here and makes validate_on_submit fail...
    #Validate on the second pass only (when button 'Bewaar' is pushed)
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        location = AssetLocation(name=form.name.data,
                                 active=form.active.data,
                                 info=form.info.data)
        db.session.add(location)
        db.session.commit()
        log.info(f'add : {location}')
        return redirect(url_for('management.asset_location.show'))
    return render_template('management/asset_location/location.html', form=form, title='Add a location', role='add', subject='management.asset_location')


@location.route('/management/asset_location/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    location = AssetLocation.query.get_or_404(id)
    form = EditForm(obj=location)
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(location)
            db.session.commit()
        return redirect(url_for('management.asset_location.show'))
    return render_template('management/asset_location/location.html', form=form, title='Edit a location', role='edit', subject='management.asset_location')


@location.route('/management/asset_location/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    location = AssetLocation.query.get_or_404(id)
    form = ViewForm(obj=location)
    if form.validate_on_submit():
        return redirect(url_for('management.asset_location.show'))
    return render_template('management/asset_location/location.html', form=form, title='View a location', role='view', subject='management.asset_location')