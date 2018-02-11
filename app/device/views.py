# -*- coding: utf-8 -*-
# app/device/views.py

import os
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db, app, _
from . import device
from ..upload import risk_analysis_path, risk_analysis_docs, photo_path, photo_docs, manual_path, manual_docs, safety_information_path, safety_information_docs
from ..models import Device

from ..base import build_filter, get_ajax_table
from ..tables_config import  tables_configuration

#This route is called by an ajax call on the assets-page to populate the table.
@device.route('/device/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['device'])

#ashow a list of purchases
@device.route('/device', methods=['GET', 'POST'])
@login_required
def devices():
    #The following line is required only to build the filter-fields on the page.
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['device'])
    return render_template('base_multiple_items.html',
                           title='devices',
                           filter=_filter, filter_form=_filter_form,
                           config = tables_configuration['device'])

#add a new device
@device.route('/device/add/<int:id>', methods=['GET', 'POST'])
@device.route('/device/add', methods=['GET', 'POST'])
@login_required
def add(id=-1):
    if id > -1:
        device = Device.query.get_or_404(int(id))
        form = AddForm(obj=device)
        #The instruction above is not perfect : it stops copying attributes a soon as it encounters an attribute in the device
        #which does not have a counterpart in the form.
        form.brand.data = device.brand
        form.type.data = device.type
        form.ce.data = device.ce
    else:
        form = AddForm()
    del form.id # is not required here and makes validate_on_submit fail...
    if not 'add' in request.form and form.validate_on_submit():
        device = Device(category=form.category.data,
                        brand=form.brand.data,
                        type=form.type.data,
                        power=form.power.data,
                        ce=form.ce.data)
        db.session.add(device)
        db.session.commit()
        #flash(_(u'You have added device {}/{}').format(device.brand, device.type))

        return redirect(url_for('device.devices'))

    return render_template('device/device.html', form=form, title=_('Add a device'), role='add', subject='device', route='device.devices')


#edit a device
@device.route('/device/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    device = Device.query.get_or_404(id)
    form = EditForm(obj=device)

    if form.validate_on_submit():
        if request.form['button'] == _(u'Save'):
            form.populate_obj(device)
            try:
                if request.files['risk_analysis_filename']:
                    filename = risk_analysis_docs.save(request.files['risk_analysis_filename'])
                if request.files['photo_filename']:
                    filename = photo_docs.save(request.files['photo_filename'])
                if request.files['manual_filename']:
                    filename = manual_docs.save(request.files['manual_filename'])
                if request.files['safety_information_filename']:
                    filename = safety_information_docs.save(request.files['safety_information_filename'])
            except Exception as e:
                flash('Cannot upload file, maybe wrong type', 'error')
            db.session.commit()
            #flash(_(u'You have edited device {}/{}').format(device.brand, device.type))

        return redirect(url_for('device.devices'))

    return render_template('device/device.html', form=form, title=_('Edit a device'), role='edit', subject='device', route='device.devices')

#no login required
@device.route('/device/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    device = Device.query.get_or_404(id)
    form = ViewForm(obj=device)
    if form.validate_on_submit():
        return redirect(url_for('device.devices'))

    return render_template('device/device.html', form=form, title=_('View a device'), role='view', subject='device', route='device.devices')

#delete a device
@device.route('/device/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    #flash(_('You have successfully deleted the device.'))

    return redirect(url_for('device.devices'))

#download a ... file
@device.route('/device/download/<string:type>/<string:file>', methods=['GET', 'POST'])
@login_required
def download(type="", file=""):
    try:
        if 'risk_analysis' in type:
            return app.send_static_file(os.path.join(risk_analysis_path, file))
        if 'photo' in type:
            return app.send_static_file(os.path.join(photo_path, file))
        if 'manual' in type:
            return app.send_static_file(os.path.join(manual_path, file))
        if 'safety_information' in type:
            return app.send_static_file(os.path.join(safety_information_path, file))
    except Exception as e:
        flash(_('Could not download file {}'.format(file)))
        flash(_('Does it still exist?'))

    return redirect(url_for('device.devices'))
