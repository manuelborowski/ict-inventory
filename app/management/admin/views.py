# -*- coding: utf-8 -*-
# app/admin/views.py

from flask import render_template, redirect, url_for, request, flash, send_file, abort
from flask_login import login_required, current_user

from . import admin
from app import db, app, log

from app.documents import  get_doc_path, get_doc_list, upload_doc, document_type_list, get_doc_select, get_doc_download

import os
import unicodecsv
from app.models import Asset, Device, Supplier, Purchase, ControlCheckTemplate, ControlCardTemplate, AssetLocation, DeviceCategory

import zipfile, xlrd

@admin.route('/management/admin', methods=['GET', 'POST'])
@login_required
def show():
    return render_template('management/admin/admin.html', mode='admin',
                           commissioning_list = get_doc_list('commissioning'),
                           photo_list = get_doc_list('photo'),
                           risk_analysis_list = get_doc_list('risk_analysis'),
                           manual_list = get_doc_list('manual'),
                           safety_information_list = get_doc_list('safety_information')
                           )

@admin.route('/management/admin/delete', methods=['GET', 'POST'])
@login_required
def delete():
    try:
        if 'delete_doc' in request.form:
            for d in document_type_list:
                if d in request.form['delete_doc']:
                    if get_doc_select(d) in request.form:
                        for i in request.form.getlist(get_doc_select(d)):
                            os.remove(os.path.join(get_doc_path(d), i))
    except Exception as e:
        flash('Kan niet verwijderen...')
    return redirect(url_for('management.admin.show'))

@admin.route('/management/admin/download', methods=['GET', 'POST'])
@login_required
def download():
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
        flash('Kan niet downloaden')
    return redirect(url_for('management.admin.show'))

@admin.route('/management/admin/upload', methods=['GET', 'POST'])
@login_required
def upload():
    try:
        upload_doc(request)
    except Exception as e:
        flash('Kan niet uploaden')
    return redirect(url_for('management.admin.show'))


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

@admin.route('/management/admin/importcsv', methods=['GET', 'POST'])
@login_required
def importcsv():
    try:
        if request.files['import_filename']:
            # format csv file :
            log.info('Import from : {}'.format(request.files['import_filename']))
            assets_file = unicodecsv.DictReader(request.files['import_filename'],  delimiter=';')
            commissioning_key_present = True if 'Indienststelling' in assets_file.fieldnames else False
            photo_key_present = True if 'Foto' in assets_file.fieldnames else False
            manual_key_present = True if 'Handleiding' in assets_file.fieldnames else False
            nbr_assets = 0
            nbr_devices = 0
            nbr_purchases = 0
            locations = AssetLocation.query.filter(AssetLocation.active).all()
            location_cache = {l.name: l for l in locations}
            device_categories = DeviceCategory.query.filter(DeviceCategory.active).filter()
            category_cache = {c.name: c for c in device_categories}
            for a in assets_file:
                #check if supplier already exists
                supplier = Supplier.query.filter(Supplier.name=='ONBEKEND').first()
                if not supplier:
                    #add a new supplier
                    supplier = Supplier(name='ONBEKEND')
                    db.session.add(supplier)
                    log.info('add: {}'.format(supplier.log()))
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
                    category = category_cache[a["Categorie"]] if a["Categorie"] in category_cache else category_cache["ANDERE"]
                    device = Device(brand=a['Merk'], category=a['Categorie'], type=a['Typenummer'], photo=photo_file, manual=manual_file,
                                    power=power, ce=True if a['CE']=='ok' else False, category_id=category.id, control_template_id=1)
                    db.session.add(device)
                    nbr_devices += 1
                    #Create a new purchase
                    purchase = Purchase.query.filter(Purchase.since=='1999/1/1').order_by(Purchase.id.desc()).first()
                    commissioning_file = a['Indienststelling'].split('\\')[-1] if commissioning_key_present else ''
                    if purchase:
                        #create a new purchase with a value +1
                        purchase = Purchase(since=purchase.since, value=int(purchase.value)+1, device=device, supplier=supplier, commissioning=commissioning_file, invoice_id=1)
                    else:
                        #add a new purchase
                        purchase = Purchase(since='1999/1/1', value='0', device=device, supplier=supplier, commissioning=commissioning_file)
                    db.session.add(purchase)
                    nbr_purchases += 1

                # check if first part of Toestel is a number, in which case it is treated as a quantity
                name = a["Toestel"]
                quantity = 1
                name_split = name.split(" ")
                if len(name_split) > 1:
                    try:
                        quantity = int(name_split[0])
                        name_split.pop(0)
                    except:
                        pass
                name = " ".join(name_split)
                location = location_cache[a["Lokaal"]] if a["Lokaal"] in location_cache else location_cache["ONBEKEND"]
                # #add the asset
                asset = Asset(name=name, status=a['Status'], serial=a['Serienummer'], location=a['Lokaal'], description=a["Beschrijving"], purchase=purchase, location_id=location.id, quantity=quantity)
                db.session.add(asset)
                nbr_assets += 1

            db.session.commit()
            log.info('import: added {} assets, {} purchases and {} devices'.format(nbr_assets, nbr_purchases, nbr_devices))

    except Exception as e:
        flash('Kan bestand niet importeren')
    return redirect(url_for('management.admin.show'))

@admin.route('/management/admin/import_controlcard_templates', methods=['GET', 'POST'])
@login_required
def import_controlcard_templates():
    try:
        if request.files['import_controlcard']:
            log.info('Import controlcard from : {}'.format(request.files['import_controlcard']))
            workbook = xlrd.open_workbook(file_contents=request.files['import_controlcard'].read())
            control_templates = ControlCardTemplate.query.all()
            template_cache = {t.name: t for t in control_templates}

            for worksheet in workbook.sheets():
                # print(worksheet.name)
                is_controlcard = False
                controlcard_row = 0
                name_found = False
                name = ''
                header_found = False
                standards = []
                checks = []
                for i in range(0, worksheet.nrows):
                    row = worksheet.row(i)

                    if not is_controlcard and row[0].ctype == xlrd.XL_CELL_TEXT and 'Controleverslag' in row[0].value:
                        controlcard_row = i
                        is_controlcard = True
                        continue

                    if not name_found and is_controlcard and row[0].ctype == xlrd.XL_CELL_TEXT and \
                            len(row[0].value.strip().split('.')) > 1:
                        name_found = True
                        name = ' '.join(row[0].value.strip().split(' ')[1:]).strip()
                        continue

                    if is_controlcard and not name_found and i > (controlcard_row + 2):
                        is_controlcard = False
                        break

                    if not header_found and name_found and len(row) > 5 and row[2].ctype == xlrd.XL_CELL_TEXT and \
                            'Ja' in row[2].value:
                        header_found = True
                        if row[1].ctype == xlrd.XL_CELL_TEXT and len(row[1].value) > 0:
                            standards.append(row[1].value.strip())
                        second_standard_row = worksheet.row(i + 1)
                        if second_standard_row[0].ctype == xlrd.XL_CELL_EMPTY and \
                                second_standard_row[1].ctype == xlrd.XL_CELL_TEXT and \
                                len(second_standard_row[1].value) > 0:
                            standards.append(second_standard_row[1].value.strip())
                        continue

                    if header_found:
                        if row[0].ctype == xlrd.XL_CELL_TEXT:
                            checks.append([row[0].value.strip(), False])
                        elif row[0].ctype == xlrd.XL_CELL_NUMBER:
                            checks.append([row[1].value.strip(), True])

                if is_controlcard:
                    if name in template_cache:
                        continue

                    template = ControlCardTemplate(name=name, info=worksheet.name.strip(), standards=', '.join(standards))
                    for i, c in enumerate(checks):
                        check = ControlCheckTemplate(name=c[0], is_check=c[1], index=i)
                        db.session.add(check)
                        template.checks.append(check)
                    template_cache[name] = template
                    db.session.add(template)

            db.session.commit()


    except Exception as e:
        flash('Kan bestand niet importeren')
    return redirect(url_for('management.admin.show'))
