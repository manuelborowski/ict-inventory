from flask import render_template, redirect, url_for, request, flash, send_file, session, make_response, jsonify
from flask_login import login_required, current_user

from .forms import AddForm, EditForm, ViewForm
from ... import db, log
from . import control
from ...models import Asset, AssetLocation, Purchase, ControlCheck, ControlStandard, ControlCardTemplate

from ...support import build_filter, get_ajax_table, get_setting_inc_index_asset_name
from ...tables_config import  tables_configuration
from ...documents import download_single_doc2

from io import StringIO
import csv, re, json

#This route is called by an ajax call on the assets-page to populate the table.
@control.route('/control/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['control'])

#show a list of assets
@control.route('/control', methods=['GET', 'POST'])
@login_required
def show():
    #The following line is required only to build the filter-fields on the page.
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['control'])
    return render_template('base_multiple_items.html',
                           title='Controle fiches',
                           filter=_filter, filter_form=_filter_form,
                           config = tables_configuration['control'],
                           )

@control.route('/control/add', methods=['GET', 'POST'])
@login_required
def add():
    pass
    # control = Asset.query.filter_by(id=int(id)).first()
    # if control:
    #     if get_setting_inc_index_asset_name():
    #         #the new name is the same as the old one, but the index is incremented
    #         #if no index available, create default 001
    #         nbr = re.search(r'\d+$', control.name)
    #         if nbr is None:
    #             control.name = control.name + '1'
    #         else:
    #             idx = int(nbr.group()) + 1
    #             control.name = control.name[:-len(nbr.group())] + str(idx)
    #     form = AddForm(obj=control)
    #     form.serial.data=''
    #     #No idea why only these 2 fields need to be copied explicitly???
    #     form.name.data = control.name
    #     form.location.data = control.location
    # else:
    #     form = AddForm()
    # if purchase_id > -1:
    #     purchase = Purchase.query.get(purchase_id)
    #     form.purchase.data = purchase
    # #Validate on the second pass only (when button 'Bewaar' is pushed)
    # if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
    #     qr_code = form.qr_code.data if form.qr_code.data != '' else None
    #     control = Asset(
    #         name=form.name.data,
    #         quantity=form.quantity.data,
    #         qr_code=qr_code,
    #         status=form.status.data,
    #         location=form.location.data,
    #         purchase=form.purchase.data,
    #         serial=form.serial.data)
    #     if 'location-id' in request.form:
    #         try:
    #             control.location_id = int(request.form['location-id'])
    #         except:
    #             unknown_location = AssetLocation.query.filter(AssetLocation.name=='ONBEKEND').first()
    #             control.location2 = unknown_location
    #     db.session.add(control)
    #     db.session.commit()
    #     db.session.refresh(control)
    #     session['asset_last_added'] = control.id
    #     log.info('add : {}'.format(control.log()))
    #     #flash(u'You have added control {}').format(control.name)
    #     return redirect(url_for('control.assets'))
    #
    # location_select = AssetLocation.get_list_for_select()
    # form.qr_code.data=qr if qr > -1 else ''
    # return render_template('control/control.html', form=form, title='Voeg activa toe', role='add', route='control.assets',
    #                        subject='control', location_select=location_select)

@control.route('/control/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    template = ControlCardTemplate.query.get_or_404(id)
    form = EditForm(obj=template)

    standard_data = [{
        'name': s.name,
        'active': s.active
    } for s in template.standards]

    check_data = [{
        'index': c.index,
        'name': c.name,
        'is_check': c.is_check,
        'active': c.active
    } for c in template.checks]

    return render_template('management/control/control.html', form=form, title='Wijzig een controle fiche',
                           role='edit', subject='management.control', route='management.control.show',
                           check_data=check_data, standard_data=standard_data)


#     control = Asset.query.get_or_404(id)
#     form = EditForm(obj=control)
#     if form.validate_on_submit():
#         if request.form['button'] == 'Bewaar':
#             form.populate_obj(control)
#             if control.qr_code=='': control.qr_code=None
#             if 'location-id' in request.form:
#                 control.location_id = int(request.form['location-id'])
#             db.session.commit()
#             log.info('edit : {}'.format(control.log()))
#             #flash'You have edited control {}').format(control.name)
#
#         return redirect(url_for('control.assets'))
#     location_select = AssetLocation.get_list_for_select()
#     return render_template('control/control.html', form=form, title='Pas een activa aan', role='edit', subject='control',
#                            route='control.assets', location_select=location_select)
#
# #no login required
@control.route('/control/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    template = ControlCardTemplate.query.get_or_404(id)
    form = ViewForm(obj=template)

#     control = Asset.query.get_or_404(id)
#     form = ViewForm(obj=control)
#     form.since.data = control.purchase.since
#     form.category.data = control.purchase.device.category
#     form.value.data = control.purchase.value
#     form.supplier.data = control.purchase.supplier
#
#     form.brand.data = control.purchase.device.brand
#     form.type.data  = control.purchase.device.type
#     form.power.data = control.purchase.device.power
#     form.ce.data  = control.purchase.device.ce
#     form.risk_analysis.data = control.purchase.device.risk_analysis
#     form.manual.data  = control.purchase.device.manual
#     form.safety_information.data = control.purchase.device.safety_information
#     form.photo.data = control.purchase.device.photo
#
#     if form.validate_on_submit():
#         return redirect(url_for('control.assets'))
#
    standard_data = [{
        'name': s.name,
        'active': s.active
    } for s in template.standards]

    check_data = [{
        'index': c.index,
        'name': c.name,
        'is_check': c.is_check,
        'active': c.active
    } for c in template.checks]

    return render_template('management/control/control.html', form=form, title='Bekijk een controle fiche',
                           role='view', subject='management.control', route='management.control.show',
                           check_data=check_data, standard_data=standard_data)
#
#
# #no login required
# @control.route('/control/qr/<string:qr>', methods=['GET', 'POST'])
# def view_via_qr(qr):
#     try:
#         control = Asset.query.filter_by(qr_code=qr).first()
#         form = ViewForm(obj=control)
#         form.since.data = control.purchase.since
#         form.category.data = control.purchase.device.category
#         form.value.data = control.purchase.value
#         form.supplier.data = control.purchase.supplier
#
#         form.brand.data = control.purchase.device.brand
#         form.type.data  = control.purchase.device.type
#         form.power.data = control.purchase.device.power
#         form.ce.data  = control.purchase.device.ce
#         form.risk_analysis.data = control.purchase.device.risk_analysis
#         form.manual.data  = control.purchase.device.manual
#         form.safety_information.data = control.purchase.device.safety_information
#         form.photo.data = control.purchase.device.photo
#     except:
#         #scanned a QR code which is not in the database yet, so it is assumed that a new control is to be added
#         copy_from_asset_id = session['asset_last_added'] if 'asset_last_added' in session else -1
#         try:
#             if current_user.is_authenticated:
#                 return redirect(url_for('control.add', id=copy_from_asset_id, qr=int(qr)))
#             else:
#                 return redirect(url_for('auth.login', redirect_url=url_for('control.add', id=copy_from_asset_id, qr=int(qr))))
#         except:
#             flash('Ongeldige QR code')
#             return redirect(url_for('auth.login'))
#
#     return render_template('control/control.html', form=form, title='Bekijk een activa', role='view', subject='control', route='control.assets')
#
# #delete an control
# @control.route('/control/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete(id):
#     control = Asset.query.get_or_404(id)
#     log.info('delete : {}'.format(control.log()))
#     db.session.delete(control)
#     db.session.commit()
#     #flash('You have successfully deleted the control.')
#
#     return redirect(url_for('control.assets'))
#
# #download a ... file
# @control.route('/control/download', methods=['GET', 'POST'])
# @login_required
# def download():
#     try:
#         return download_single_doc2(request)
#     except Exception as e:
#         flash('Kan niet downloaden  ')
#     return ('', 204)

# #export a list of assets
# @control.route('/control/export', methods=['GET', 'POST'])
# @login_required
# def exportcsv():
#     try:
#         #The following line is required only to build the filter-fields on the page.
#         __filters_enabled,  _filter_forms, _filtered_list, _total_count, _filtered_count = build_filter(tables_configuration['control'])
#         headers = [
#             'name',
#             'category',
#             'location',
#             'since',
#             'value',
#             'qr',
#             'status',
#             'supplier',
#             'brand',
#             'type',
#             'serial',
#             'power',
#             'ce',
#         ]
#
#         rows = []
#         for a in _filtered_list:
#             rows.append((
#                 a.name,
#                 a.purchase.device.category,
#                 a.location,
#                 a.purchase.since,
#                 a.purchase.value,
#                 a.qr_code,
#                 a.status,
#                 a.purchase.supplier.name,
#                 a.purchase.device.brand,
#                 a.purchase.device.type,
#                 a.serial,
#                 a.purchase.device.power,
#                 a.purchase.device.ce
#             ))
#         si = StringIO()
#         cw = csv.writer(si, delimiter=';')
#         cw.writerow(headers)
#         cw.writerows(rows)
#         output = make_response(si.getvalue())
#         output.headers["Content-Disposition"] = "attachment; filename=assets.csv"
#         output.headers["Content-type"] = "text/csv"
#         return output
#     except Exception as e:
#         log.error('Could not export file {}'.format(e))
#         return redirect(url_for('control.assets'))
#
