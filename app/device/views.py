from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db, log
from . import device
from ..documents import upload_doc
from ..models import Device

from ..support import build_filter, get_ajax_table
from ..tables_config import  tables_configuration
import json

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
                           title='toestellen',
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
    #Validate on the second pass only (when button 'Bewaar' is pushed)
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        device = Device(
                        category_id=form.category_id.data,
                        brand=form.brand.data,
                        type=form.type.data,
                        power=form.power.data,
                        ce=form.ce.data,
                        manual=form.manual.data,
                        risk_analysis=form.risk_analysis.data,
                        safety_information=form.safety_information.data,
                        photo=form.photo.data,
                        control_template=form.control_template.data,
                        )
        db.session.add(device)
        db.session.commit()
        log.info('add: {}'.format(device.log()))
        #flash(_(u'You have added device {}/{}').format(device.brand, device.type))

        return redirect(url_for('device.devices'))

    return render_template('device/device.html', form=form, title='Voeg een toestel toe', role='add', subject='device', route='device.devices')


#edit a device
@device.route('/device/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    device = Device.query.get_or_404(id)
    form = EditForm(obj=device)

    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(device)
            db.session.commit()
            #flash(_(u'You have edited device {}/{}').format(device.brand, device.type))
        return redirect(url_for('device.devices'))

    return render_template('device/device.html', form=form, title='Pas een toestel aan', role='edit', subject='device', route='device.devices')

#no login required
@device.route('/device/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    device = Device.query.get_or_404(id)
    form = ViewForm(obj=device)
    if form.validate_on_submit():
        return redirect(url_for('device.devices'))

    return render_template('device/device.html', form=form, title='Bekijk een toestel', role='view', subject='device', route='device.devices')

#delete a device
@device.route('/device/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    device = Device.query.get_or_404(id)
    log.info('delete: {}'.format(device.log()))
    db.session.delete(device)
    db.session.commit()
    #flash(_('You have successfully deleted the device.'))

    return redirect(url_for('device.devices'))

@device.route('/device/ajax_request/<string:jds>', methods=['GET', 'POST'])
@login_required
def ajax_request(jds):
    try:
        jd = json.loads(jds)
        if jd['action'] == 'get-device-list':
            data = {
                'device_options': Device.get_list_for_select_first_empty(int(jd['category-id'])),
                'opaque': jd['opaque'],
            }
            return jsonify({"status": True, "data": data})
    except Exception as e:
        return jsonify({"status": False, 'details': f'{e}'})
    return jsonify({"status": False, 'details': f'Er is iets fout gegaan met action: {jd["action"]}\n{jds}'})

