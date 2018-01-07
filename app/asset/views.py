# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, flash, redirect, url_for, request, jsonify, get_flashed_messages, session
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db, _
from . import asset
from ..models import Asset

from ..base import build_filter, asset_template

#This route is called by an ajax call on the assets-page to populate the table.
@asset.route('/asset/data', methods=['GET', 'POST'])
@login_required
def source_data():
    assets, tc, fc, filter = build_filter(Asset, asset_template,
                                  since=True, value=True, location=True, category=True, status=True, supplier=True, device=True)
    assets_dict = [a.ret_dict() for a in assets]
    for a in assets_dict:
        a['name'] = "<a href=\"{}\">{}</a>".format(url_for('asset.view', id=a['id']), a['name'])
        a['DT_RowId'] = a['id']
    output = {}
    output['draw'] = str(int(request.values['draw']))
    output['recordsTotal'] = str(tc)
    output['recordsFiltered'] = str(fc)
    output['data'] = assets_dict
    #add the (non-standard) flash-tag to display flash-messages via ajax
    fml = get_flashed_messages()
    if not not fml:
        output['flash'] = fml
    return jsonify(output)

#add a new asset
@asset.route('/asset', methods=['GET', 'POST'])
@login_required
def assets():
    #The following line is required only to build the filter-fields on the page.
    assets, tc, fc, filter = build_filter(Asset, asset_template,
                                  since=True, value=True, location=True, category=True, status=True, supplier=True, device=True)
    return render_template('base_multiple_items.html', title='assets', route='asset.assets', subject='asset',
                           header_list=asset_template, filter=filter)

#add a new asset
@asset.route('/asset/add/<int:id>', methods=['GET', 'POST'])
@asset.route('/asset/add', methods=['GET', 'POST'])
@login_required
def add(id=-1):
    print '>>>>>>>>>>>>> REQUEST.FORM {}'.format(request.form)
    print '>>>>>>>>>>>>> REQUEST.VALUES {}'.format(request.values)
    print '>>>>>>>>>>>>> ID {}'.format(id)
    #qr_code can be inserted in 2 forms :
    #regular number, e.g. 433
    #complete url, e.g. http://blabla.com/qr/433.  If it contains http.*qr/, extract the number after last slash.
    if id > -1:
        asset = Asset.query.get_or_404(int(id))
    # if 'copy_from' in request.form:
    #     asset = Asset.query.get_or_404(int(request.form['copy_from']))
        form = AddForm(obj=asset)
        form.qr_code.data=''
        form.serial.data=''
        #No idea why only these 2 fields need to be copied explicitly???
        form.name.data = asset.name
        form.location.data = asset.location
    else:
        form = AddForm()
    del form.id # is not required here and makes validate_on_submit fail...
    if not 'add' in request.form and form.validate_on_submit():
        asset = Asset(name=form.name.data,
                        qr_code=form.qr_code.data,
                        status=form.status.data,
                        location=form.location.data,
                        purchase=form.purchase.data,
                        serial=form.serial.data)
        db.session.add(asset)
        db.session.commit()
        print '>>>>>>>>>> ASSET SAVED'
        #flash(_(u'You have added asset {}').format(asset.name))

        return redirect(url_for('asset.assets'))

    return render_template('asset/asset.html', form=form, title=_(u'Add an asset'), role='add', route='asset.assets', subject='asset')

#edit a asset
@asset.route('/asset/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    asset = Asset.query.get_or_404(id)
    form = EditForm(obj=asset)
    if form.validate_on_submit():
        if request.form['button'] == _(u'Save'):
            form.populate_obj(asset)
            db.session.commit()
            #flash(_(u'You have edited asset {}').format(asset.name))

        return redirect(url_for('asset.assets'))

    return render_template('asset/asset.html', form=form, title=_(u'Edit an asset'), role='edit', subject='asset', route='asset.assets')

#no login required
@asset.route('/asset/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    asset = Asset.query.get_or_404(id)
    form = ViewForm(obj=asset)
    form.since.data = asset.purchase.since
    form.category.data = asset.purchase.device.category
    form.value.data = asset.purchase.value
    form.supplier.data = asset.purchase.supplier
    if form.validate_on_submit():
        return redirect(url_for('asset.assets'))

    return render_template('asset/asset.html', form=form, title=_(u'View an asset'), role='view', subject='asset', route='asset.assets')


#no login required
@asset.route('/asset/qr/<string:qr>', methods=['GET', 'POST'])
def view_via_qr(qr):
    asset = Asset.query.filter_by(qr_code=qr).first_or_404()
    form = ViewForm(obj=asset)
    form.since.data = asset.purchase.since
    form.category.data = asset.purchase.device.category
    form.value.data = asset.purchase.value
    form.supplier.data = asset.purchase.supplier
    return render_template('asset/asset.html', form=form, title=_(u'View an asset'), role='view', subject='asset', route='asset.assets')

#delete an asset
@asset.route('/asset/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    #flash(_('You have successfully deleted the asset.'))

    return redirect(url_for('asset.assets'))

