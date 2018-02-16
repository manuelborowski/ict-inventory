# -*- coding: utf-8 -*-
# app/admin/views.py

from flask import render_template, redirect, url_for, request, flash, send_file, abort
from flask_login import login_required, current_user

from . import admin
from .. import db, app

from ..documents import  get_doc_path, get_doc_list, upload_doc, document_type_list, get_doc_select, get_doc_download

import os
import unicodecsv  as  csv
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
                elif len(sl) > 1:
                    zf_name = d + '.zip'
                    zf = zipfile.ZipFile(zf_name, 'w', zipfile.ZIP_DEFLATED)
                    for i in sl:
                        zf.write(os.path.join(app.root_path, '..', get_doc_path(d), i), arcname=os.path.join(d,i))
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
        upload_doc(request)
    except Exception as e:
        flash('Could not upload')
    return redirect(url_for('admin.show'))


#Toestel        name
#Categorie      category
#Status         status
#Merk           brand
#Typenummer     type
#Serienummer    serial
#Vermogen       power
#Lokaal         location
#Foto           photo
#Handleiding    manual
#CE             ce
#Indienststelling   commissioning

@admin.route('/admin/importcsv', methods=['GET', 'POST'])
@login_required
def importcsv():
    check_admin()
    try:
        if request.files['import_filename']:
            # format csv file :
            assets_file = csv.DictReader(request.files['import_filename'],  delimiter=';', encoding='utf-8-sig')
            commissioning_key_present = True if 'Indienststelling' in assets_file.fieldnames else False
            photo_key_present = True if 'Foto' in assets_file.fieldnames else False
            manual_key_present = True if 'Handleiding' in assets_file.fieldnames else False
            for a in assets_file:
                #check if supplier already exists
                supplier = Supplier.query.filter(Supplier.name=='ONBEKEND').first()
                if not supplier:
                    #add a new supplier
                    supplier = Supplier(name='ONBEKEND')
                    db.session.add(supplier)
                #check if device already exists
                device = Device.query.filter(Device.brand==a['Merk'], Device.type==a['Typenummer']).first()
                if device:
                    purchase = Purchase.query.filter(Purchase.device==device).first()
                else:
                    #add a new device
                    try:
                        power = int(a['Vermogen'])
                    except:
                        power = 0

                    photo_file = a['Foto'].split('\\')[-1] if photo_key_present else ''
                    manual_file = a['Handleiding'].split('\\')[-1] if manual_key_present else ''
                    device = Device(brand=a['Merk'], category=a['Categorie'], type=a['Typenummer'], photo=photo_file, manual=manual_file,
                                    power=power, ce=True if a['CE']=='ok' else False)
                    db.session.add(device)
                    #Create a new purchase
                    purchase = Purchase.query.filter(Purchase.since=='1999/1/1').order_by('-id').first()
                    commissioning_file = a['Indienststelling'].split('\\')[-1] if commissioning_key_present else ''
                    if purchase:
                        #create a new purchase with a value +1
                        purchase = Purchase(since = purchase.since, value = int(purchase.value)+1, device=device, supplier=supplier, commissioning=commissioning_file)
                    else:
                        #add a new purchase
                        purchase = Purchase(since='1999/1/1', value='0', device=device, supplier=supplier, commissioning=commissioning_file)
                    db.session.add(purchase)
                # #add the asset
                asset = Asset(name=a['Toestel'], status=a['Status'], serial=a['Serienummer'], location=a['Lokaal'], purchase=purchase)
                db.session.add(asset)

            db.session.commit()

    except Exception as e:
        flash('Could not import file')
    return redirect(url_for('admin.show'))
