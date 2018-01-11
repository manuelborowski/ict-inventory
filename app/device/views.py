# -*- coding: utf-8 -*-
# app/device/views.py

from flask import render_template, redirect, url_for, request
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db, _
from . import device
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
    __filter, __filter_form, a,b, c = build_filter(tables_configuration['device'])
    return render_template('base_multiple_items.html', title='devices', route='device.devices', subject='device',
                           header_list=tables_configuration['device']['template'], filter=__filter, filter_form=__filter_form,
                           delete_message="Are you sure you want to delete this device AND all associated purchases AND assets?")

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

