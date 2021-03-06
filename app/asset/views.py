# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, redirect, url_for, request, flash, send_file, session, make_response, jsonify
from flask_login import login_required, current_user

from .forms import AddForm, EditForm, ViewForm
from .. import db, log
from . import asset
from ..models import Asset, AssetLocation, Purchase

from ..support import build_filter, get_ajax_table, get_setting_inc_index_asset_name
from ..tables_config import  tables_configuration
from ..documents import download_single_doc2

from io import StringIO
import csv, re, json

#This route is called by an ajax call on the assets-page to populate the table.
@asset.route('/asset/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['asset'])

#show a list of assets
@asset.route('/asset', methods=['GET', 'POST'])
@asset.route('/asset/<int:purchase_id>', methods=['GET', 'POST'])
@login_required
def assets(purchase_id=None):
    #The following line is required only to build the filter-fields on the page.
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['asset'])
    default_filter_values = {}
    if purchase_id:
        default_filter_values['purchase_id'] = purchase_id
    return render_template('base_multiple_items.html',
                           title='activa',
                           filter=_filter, filter_form=_filter_form,
                           config = tables_configuration['asset'],
                           default_filter_values=default_filter_values,
                           purchase_id=purchase_id)

#export a list of assets
@asset.route('/asset/export', methods=['GET', 'POST'])
@login_required
def exportcsv():
    try:
        #The following line is required only to build the filter-fields on the page.
        __filters_enabled,  _filter_forms, _filtered_list, _total_count, _filtered_count = build_filter(tables_configuration['asset'])
        headers = [
            'name',
            'category',
            'location',
            'since',
            'value',
            'qr',
            'status',
            'supplier',
            'brand',
            'type',
            'serial',
            'power',
            'ce',
        ]

        rows = []
        for a in _filtered_list:
            rows.append((
                a.name,
                a.purchase.device.category,
                a.location,
                a.purchase.since,
                a.purchase.value,
                a.qr_code,
                a.status,
                a.purchase.supplier.name,
                a.purchase.device.brand,
                a.purchase.device.type,
                a.serial,
                a.purchase.device.power,
                a.purchase.device.ce
            ))
        si = StringIO()
        cw = csv.writer(si, delimiter=';')
        cw.writerow(headers)
        cw.writerows(rows)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=assets.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    except Exception as e:
        log.error('Could not export file {}'.format(e))
        return redirect(url_for('asset.assets'))

#add a new asset
@asset.route('/asset/add/<int:id>/<int:qr>/<int:purchase_id>', methods=['GET', 'POST'])
@asset.route('/asset/add/<int:id>/<int:qr>', methods=['GET', 'POST'])
@asset.route('/asset/add/<int:id>', methods=['GET', 'POST'])
@asset.route('/asset/add', methods=['GET', 'POST'])
@login_required
def add(id=-1, qr=-1, purchase_id=-1):
    #qr_code can be inserted in 2 forms :
    #regular number, e.g. 433
    #complete url, e.g. http://blabla.com/qr/433.  If it contains http.*qr/, extract the number after last slash.
    asset = Asset.query.filter_by(id=int(id)).first()
    if asset:
        if get_setting_inc_index_asset_name():
            #the new name is the same as the old one, but the index is incremented
            #if no index available, create default 001
            nbr = re.search(r'\d+$', asset.name)
            if nbr is None:
                new_asset_name = asset.name + '001'
            else:
                idx = int(nbr.group()) + 1
                idx_len = len(nbr.group())
                new_asset_name = asset.name[:-idx_len] + f'{idx:0{idx_len}d}'
        form = AddForm()
        form.serial.data = ''
        form.qr_code.data = ''
        form.quantity.data = asset.quantity
        form.purchase.data = asset.purchase
        form.status.data = asset.status
        #No idea why only these 2 fields need to be copied explicitly???
        form.name.data = new_asset_name
        form.location.data = asset.location2.name
        form.location_id.data = asset.location2.id
    else:
        form = AddForm()
    if purchase_id > -1:
        purchase = Purchase.query.get(purchase_id)
        form.purchase.data = purchase
    #Validate on the second pass only (when button 'Bewaar' is pushed)
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        qr_code = form.qr_code.data if form.qr_code.data != '' else None
        asset = Asset(
            name=form.name.data,
            quantity=form.quantity.data,
            qr_code=qr_code,
            status=form.status.data,
            location=form.location.data,
            purchase=form.purchase.data,
            serial=form.serial.data)
        if  form.location_id.data > -1:
            asset.location_id = form.location_id.data
        else:
            unknown_location = AssetLocation.query.filter(AssetLocation.name=='ONBEKEND').first()
            asset.location_id = unknown_location.id
        db.session.add(asset)
        db.session.commit()
        db.session.refresh(asset)
        session['asset_last_added'] = asset.id
        log.info('add : {}'.format(asset.log()))
        #flash(u'You have added asset {}').format(asset.name)
        return redirect(url_for('asset.assets'))

    location_select = AssetLocation.get_list_for_select()
    form.qr_code.data=qr if qr > -1 else ''
    return render_template('asset/asset.html', form=form, title='Voeg activa toe', role='add', route='asset.assets',
                           subject='asset', location_select=location_select)

#edit a asset
@asset.route('/asset/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    asset = Asset.query.get_or_404(id)
    form = EditForm(obj=asset)
    form.location.data = asset.location2.name
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(asset)
            if asset.qr_code=='': asset.qr_code=None
            if form.location_id.data > -1:
                asset.location_id = form.location_id.data
            db.session.commit()
            log.info('edit : {}'.format(asset.log()))
            #flash'You have edited asset {}').format(asset.name)

        return redirect(url_for('asset.assets'))
    location_select = AssetLocation.get_list_for_select()
    return render_template('asset/asset.html', form=form, title='Pas een activa aan', role='edit', subject='asset',
                           route='asset.assets', location_select=location_select)

#no login required
@asset.route('/asset/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    asset = Asset.query.get_or_404(id)
    form = ViewForm(obj=asset)
    form.since.data = asset.purchase.since
    form.category.data = asset.purchase.device.category
    form.value.data = str(float(asset.purchase.asset_value)).replace('.', ',')
    form.supplier.data = asset.purchase.supplier
    form.location.data = asset.location2.name
    form.location_id.data = asset.location2.id

    form.brand.data = asset.purchase.device.brand
    form.type.data  = asset.purchase.device.type
    form.power.data = asset.purchase.device.power
    form.ce.data  = asset.purchase.device.ce
    form.risk_analysis.data = asset.purchase.device.risk_analysis
    form.manual.data  = asset.purchase.device.manual
    form.safety_information.data = asset.purchase.device.safety_information
    form.photo.data = asset.purchase.device.photo

    if form.validate_on_submit():
        return redirect(url_for('asset.assets'))

    return render_template('asset/asset.html', form=form, title='Bekijk een activa', role='view', subject='asset', route='asset.assets')


#no login required
@asset.route('/asset/qr/<string:qr>', methods=['GET', 'POST'])
def view_via_qr(qr):
    try:
        asset = Asset.query.filter_by(qr_code=qr).first()
        form = ViewForm(obj=asset)
        form.since.data = asset.purchase.since
        form.category.data = asset.purchase.device.category
        form.value.data = asset.purchase.value
        form.supplier.data = asset.purchase.supplier

        form.brand.data = asset.purchase.device.brand
        form.type.data  = asset.purchase.device.type
        form.power.data = asset.purchase.device.power
        form.ce.data  = asset.purchase.device.ce
        form.risk_analysis.data = asset.purchase.device.risk_analysis
        form.manual.data  = asset.purchase.device.manual
        form.safety_information.data = asset.purchase.device.safety_information
        form.photo.data = asset.purchase.device.photo
    except:
        #scanned a QR code which is not in the database yet, so it is assumed that a new asset is to be added
        copy_from_asset_id = session['asset_last_added'] if 'asset_last_added' in session else -1
        try:
            if current_user.is_authenticated:
                return redirect(url_for('asset.add', id=copy_from_asset_id, qr=int(qr)))
            else:
                return redirect(url_for('auth.login', redirect_url=url_for('asset.add', id=copy_from_asset_id, qr=int(qr))))
        except:
            flash('Ongeldige QR code')
            return redirect(url_for('auth.login'))

    return render_template('asset/asset.html', form=form, title='Bekijk een activa', role='view', subject='asset', route='asset.assets')

#delete an asset
@asset.route('/asset/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    asset = Asset.query.get_or_404(id)
    log.info('delete : {}'.format(asset.log()))
    db.session.delete(asset)
    db.session.commit()
    #flash('You have successfully deleted the asset.')

    return redirect(url_for('asset.assets'))

#download a ... file
@asset.route('/asset/download', methods=['GET', 'POST'])
@login_required
def download():
    try:
        return download_single_doc2(request)
    except Exception as e:
        flash('Kan niet downloaden  ')
    return ('', 204)


@asset.route('/asset/add_inspection/<int:id>', methods=['GET', 'POST'])
@login_required
def add_inspection(id=-1):
    asset = Asset.query.get(id)
    control_template = asset.purchase.device.control_template
    if control_template.name == 'NVT':
        flash("Je kan geen inspectie doen op deze activa")
        return redirect(url_for('asset.assets'))
    return redirect(url_for('inspect.add_from_asset', asset_id=id))

@asset.route('/asset/inspection_overview/<int:id>', methods=['GET', 'POST'])
@login_required
def inspection_overview(id=-1):
    asset = Asset.query.get(id)
    control_template = asset.purchase.device.control_template
    if control_template.name == 'NVT':
        flash("Deze activa heeft geen inspecties")
        return redirect(url_for('asset.assets'))
    return redirect(url_for('inspect.overview_from_asset', asset_id=id))
