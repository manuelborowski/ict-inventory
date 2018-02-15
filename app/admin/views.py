# -*- coding: utf-8 -*-
# app/admin/views.py

from flask import render_template, redirect, url_for, request, flash, send_file, abort
from flask_login import login_required, current_user

from . import admin
from .. import db, app

from ..documents import get_doc_reference, get_doc_path, get_doc_list
from ..documents import document_type_list, get_doc_filename, get_doc_select, get_doc_download, get_doc_delete

import os, csv
from ..models import Asset, Device, Supplier, Purchase

import zipfile

def check_admin():
    if not current_user.is_admin:
        abort(403)

@admin.route('/admin', methods=['GET', 'POST'])
@login_required
def show():
    check_admin()

    return render_template('admin/admin.html', mode='admin',
                           commissioning_list = get_doc_list('commissioning'),
                           photo_list = get_doc_list('photo'),
                           risk_analysis_list = get_doc_list('risk_analysis'),
                           manual_list = get_doc_list('manual'),
                           safety_information_list = get_doc_list('safety_information')
                           )

@admin.route('/admin/delete', methods=['GET', 'POST'])
@login_required
def delete():
    check_admin()
    try:
        if 'delete_doc' in request.form:
            for d in document_type_list:
                if d in request.form['delete_doc']:
                    if get_doc_select(d) in request.form:
                        for i in request.form.getlist(get_doc_select(d)):
                            os.remove(os.path.join(get_doc_path(d), i))
    except Exception as e:
        flash('Could not delete...')
    return redirect(url_for('admin.show'))

@admin.route('/admin/download', methods=['GET', 'POST'])
@login_required
def download():
    check_admin()
    try:
        for d in document_type_list:
            if get_doc_download(d) in request.form:
                sl = request.form.getlist(get_doc_select(d))
                if len(sl) == 1:
                    return send_file(os.path.join(app.root_path, '..', get_doc_path(d), sl[0]), as_attachment=True)
                else:
                    zf_name = d + '.zip'
                    zf = zipfile.ZipFile(zf_name, 'w', zipfile.ZIP_DEFLATED)
                    for i in sl:
                        zf.write(os.path.join(app.root_path, '..', get_doc_path(d), i), arcname=i)
                    zf.close()
                    return send_file(os.path.join(app.root_path, '..', zf_name), mimetype='zip', as_attachment=True)
    except Exception as e:
        flash('Could not download')
    return redirect(url_for('admin.show'))

@admin.route('/admin/upload', methods=['GET', 'POST'])
@login_required
def upload():
    check_admin()
    try:
        for d in document_type_list:
            if request.files[get_doc_filename(d)]:
                for f in request.files.getlist(get_doc_filename(d)):
                    filename = get_doc_reference(d).save(f)
    except Exception as e:
        flash('Could not upload')
    return redirect(url_for('admin.show'))


@admin.route('/admin/importcsv', methods=['GET', 'POST'])
@login_required
def importcsv():
    check_admin()
    try:
        if request.files['import_filename']:
            # format csv file :
            # 0:name, 1:category, 2:status, 3:brand, 4:type, 5:serial, 6:power, 7:location, 8:photo, 9:manual, 10:ce
            assets_file = csv.reader(request.files['import_filename'],  delimiter=';')
            #skip first line
            next(assets_file)
            for a in assets_file:
                #check if supplier already exists
                supplier = Supplier.query.filter(Supplier.name=='ONBEKEND').first()
                if not supplier:
                    #add a new supplier
                    supplier = Supplier(name='ONBEKEND')
                    db.session.add(supplier)
                #check if device already exists
                device = Device.query.filter(Device.brand==a[3], Device.type==a[4]).first()
                if device:
                    purchase = Purchase.query.filter(Purchase.device==device).first()
                else:
                    #add a new device
                    try:
                        power = int(a[6])
                    except:
                        power = 0
                    device = Device(brand=a[3], category=a[1], type=a[4], photo=a[8], power=power, ce=True if a[10]=='ok' else False)
                    db.session.add(device)
                    #Create a new purchase
                    purchase = Purchase.query.filter(Purchase.since=='1999/1/1').order_by('-id').first()
                    if purchase:
                        #create a new purchase with a value +1
                        purchase = Purchase(since = purchase.since, value = int(purchase.value)+1, device=device, supplier=supplier)
                    else:
                        #add a new purchase
                        purchase = Purchase(since='1999/1/1', value='0', device=device, supplier=supplier)
                    db.session.add(purchase)
                # #add the asset
                asset = Asset(name=a[0], status=a[2], serial=a[5], location=a[7], purchase=purchase)
                db.session.add(asset)

            db.session.commit()

    except Exception as e:
        flash('Could not import file')
    return redirect(url_for('admin.show'))
