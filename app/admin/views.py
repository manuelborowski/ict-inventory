# -*- coding: utf-8 -*-
# app/admin/views.py

from flask import render_template, redirect, url_for, request, flash, send_file, abort
from flask_login import login_required, current_user

from . import admin
from .. import db

from ..upload import get_commissioning_docs, commissioning_docs, get_photo_docs, photo_docs, get_risk_analysis_docs, risk_analysis_docs
from ..upload import get_manual_docs, manual_docs, get_safety_information_docs, safety_information_docs

import cStringIO, csv
from ..models import Asset, Device, Supplier, Purchase

def check_admin():
    if not current_user.is_admin:
        abort(403)

@admin.route('/admin', methods=['GET', 'POST'])
@login_required
def show():
    check_admin()

    return render_template('admin/admin.html', mode='admin',
                           commissioning_list = get_commissioning_docs(),
                           photo_list = get_photo_docs(),
                           risk_analysis_list = get_risk_analysis_docs(),
                           manual_list = get_manual_docs(),
                           safety_information_list = get_safety_information_docs()
                           )

@admin.route('/admin/importcsv', methods=['GET', 'POST'])
@login_required
def importcsv():
    check_admin()
    print '>>>>>>>> REQUEST.FILES {}'.format(request.files)
    print '>>>>>>>> REQUEST.FORM {}'.format(request.form)

    try:
        if request.files['commissioning_filename']:
            for f in request.files.getlist('commissioning_filename'):
                filename = commissioning_docs.save(f)

        if request.files['risk_analysis_filename']:
            for f in request.files.getlist('risk_analysis_filename'):
                filename = risk_analysis_docs.save(f)

        if request.files['photo_filename']:
            for f in request.files.getlist('photo_filename'):
                filename = photo_docs.save(f)

        if request.files['manual_filename']:
            for f in request.files.getlist('manual_filename'):
                filename = manual_docs.save(f)

        if request.files['safety_information_filename']:
            for f in request.files.getlist('safety_information_filename'):
                filename = safety_information_docs.save(f)

        if request.files['import_filename']:
            # format csv file :
            # 0:name, 1:category, 2:status, 3:brand, 4:type, 5:serial, 6:power, 7:location, 8:photo, 9:manual, 10:ce
            print '>>>>>>>>>>> IMPORT CSV {}'.format(request.files  )
            assets_file = csv.reader(request.files['import_filename'],  delimiter=';')
            #skip first line
            next(assets_file)
            for a in assets_file:
                #check if supplier already exists
                supplier = Supplier.query.filter(Supplier.name=='school').first()
                if not supplier:
                    #add a new supplier
                    supplier = Supplier(name='school')
                    db.session.add(supplier)
                    print supplier
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
                    print(device)
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
                print purchase
                # #add the asset
                asset = Asset(name=a[0], status=a[2], serial=a[5], location=a[7], purchase=purchase)
                db.session.add(asset)
                print asset

            db.session.commit()

    except Exception as e:
        print str(e)
        flash('Could not import file')
    return redirect(url_for('admin.show'))
