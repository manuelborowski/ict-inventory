# -*- coding: utf-8 -*-
# app/device/views.py

from flask import render_template, render_template_string, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user
from flask_table import Table, Col, DateCol, LinkCol

import datetime, time

from .forms import AddForm, EditForm, ViewForm
from .. import db, _
from . import device
from ..models import Device


#Special column to add html-tags.  Note : this can be dangerous, so whatch out!!!
class NoEscapeCol(Col):
    def td_format(self, content):
        return content

class DeviceTable(Table):

    category = Col(_(u'Category'))    # one of: PC, BEAMER, PRINTER, ANDERE
    brand = Col(_(u'Brand'))
    type = Col(_(u'Type'))
    power = Col(_(u'Power'))
    ce = Col(_(u'CE'))
    delete = NoEscapeCol('')
    edit = NoEscapeCol('')
    view = NoEscapeCol('')
    id = Col('Id')
    copy_from = NoEscapeCol('C')
    classes = ['table ' 'table-striped ' 'table-bordered ']
    html_attrs = {'id': 'devicetable', 'cellspacing': '0', 'width': '100%'}

def check_value_in_form(value_key, form):
    if value_key in form and form[value_key] != '':
        try:
            float(form[value_key])
            return form[value_key]
        except:
            flash(_(u'Wrong value format'))
    return None



@device.route('/device', methods=['GET', 'POST'])
@login_required
def devices():
    devices = Device.query.all()
    for d in devices:
        d.copy_from = render_template_string("<input type='radio' name='copy_from' value='" + str(d.id) + "'>")
        d.delete = render_template_string("<a class='confirmBeforeDelete' u_id=" + str(d.id) + "><i class='fa fa-trash'></i></a>")
        d.edit = render_template_string("<a href=\"{{ url_for('device.edit', id=" + str(d.id) + ") }}\"><i class='fa fa-pencil'></i>")
        d.view = render_template_string("<a href=\"{{ url_for('device.view', id=" + str(d.id) + ") }}\"><i class='fa fa-eye'></i>")
    device_table = DeviceTable(devices)

    return render_template('device/devices.html', title='devices', device_table = device_table, table_id='devicetable', filter=filter)


#add a new device
@device.route('/device/add', methods=['GET', 'POST'])
@login_required
def add():
    if 'copy_from' in request.form:
        device = Device.query.get_or_404(int(request.form['copy_from']))
        form = AddForm(obj=device)
        #No idea why only these 2 fields need to be copied explicitly???
        #form.name.data = asset.name
        #form.location.data = asset.location
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
        flash(_(u'You have added device {}/{}').format(device.brand, device.type))

        return redirect(url_for('device.devices'))

    return render_template('device/device.html', form=form, title=_(u'Add'))


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
            flash(_(u'You have edited device {}/{}').format(device.brand, device.type))

        return redirect(url_for('device.devices'))

    return render_template('device/device.html', form=form, title=_(u'Edit'))

#no login required
@device.route('/device/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    device = Device.query.get_or_404(id)
    form = ViewForm(obj=device)
    if form.validate_on_submit():
        return redirect(url_for('device.devices'))

    return render_template('device/device.html', form=form, title=_(u'View'))

#delete a device
@device.route('/device/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    flash(_('You have successfully deleted the device.'))

    return redirect(url_for('device.devices'))

