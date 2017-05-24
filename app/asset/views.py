# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, render_template_string, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user
from flask_table import Table, Col, DateCol

import datetime, time

from .forms import AddForm, EditForm, ViewForm
from .. import db
from . import asset
from ..models import Asset


#Special column to add html-tags.  Note : this can be dangerous, so whatch out!!!
class NoEscapeCol(Col):
    def td_format(self, content):
        return content

class AssetTable(Table):
    id = Col('Id')
    name = Col('Name')        # eg PC245
    date_in_service = DateCol('Since', date_format='dd-MM-YYYY')
    qr_code = Col('QR')
    category = Col('Category')    # one of: PC, BEAMER, PRINTER, ANDERE
    status = Col('Status')    # one of: IN_DIENST, HERSTELLING, STUK, TE_VERVANGEN, ANDERE
    value = Col('Value')      # value in euro
    location = Col('Location')    # eg E203
    #picture = Col('Picture')    # path to picture on disk
    #db_status = Col('DB status')    # one of: NIEW, ACTIEF, ANDERE
    #description = Col('Description')
    supplier = Col('Supplier')
    delete = NoEscapeCol('')
    edit = NoEscapeCol('')
    view = NoEscapeCol('')
    classes = ['table ' 'table-striped ' 'table-bordered ']
    html_attrs = {'id': 'assettable', 'cellspacing': '0', 'width': '100%'}


def check_date_in_form(date_key, form):
    if date_key in form and form[date_key] != '':
        try:
            time.strptime(form[date_key], '%d-%M-%Y')
            return form[date_key]
        except:
            flash('Wrong date format, must be of form d-m-y')
    return None

def check_value_in_form(value_key, form):
    if value_key in form and form[value_key] != '':
        try:
            float(form[value_key])
            return form[value_key]
        except:
            flash('Wrong value format')
    return None


class Filter():
    date_after = ''
    date_before = ''
    value_from = ''
    value_till = ''

@asset.route('/asset', methods=['GET', 'POST'])
@login_required
def assets():
    print(request.form)
    filter = Filter()
    assets = Asset.query
    date = check_date_in_form('date_after', request.form)
    if date:
        assets = assets.filter(Asset.date_in_service > Asset.reverse_date(date))
        filter.date_after=date
    date = check_date_in_form('date_before', request.form)
    if date:
        assets = assets.filter(Asset.date_in_service < Asset.reverse_date(date))
        filter.date_before=date
    value = check_value_in_form('value_from', request.form)
    if value:
        assets = assets.filter(Asset.value > value)
        filter.value_from = value
    value = check_value_in_form('value_till', request.form)
    if value:
        assets = assets.filter(Asset.value < value)
        filter.value_till = value
    assets=assets.all()
    for a in assets:
        a.delete = render_template_string("<a class='confirmBeforeDelete' u_id=" + str(a.id) + "><i class='fa fa-trash'></i></a>")
        a.edit = render_template_string("<a href=\"{{ url_for('asset.edit', id=" + str(a.id) + ") }}\"><i class='fa fa-pencil'></i>")
        a.view = render_template_string("<a href=\"{{ url_for('asset.view', id=" + str(a.id) + ") }}\"><i class='fa fa-eye'></i>")
    asset_table = AssetTable(assets)

    return render_template('asset/assets.html', title='assets', asset_table=asset_table, table_id='assettable', filter=filter)


#add a new asset
@asset.route('/asset/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    del form.id # is not required here and makes validate_on_submit fail...
    #qr_code can be inserted in 2 forms :
    #regular number, e.g. 433
    #complete url, e.g. http://blabla.com/qr/433.  If it contains http.*qr/, extract the number after last slash.

    if form.validate_on_submit():
        asset = Asset(name=form.name.data,
                        date_in_service=form.date_in_service.data,
                        qr_code=form.qr_code.data,
                        category=form.category.data,
                        status=form.status.data,
                        value=form.value.data,
                        location=form.location.data,
                        picture=form.picture.data,
                        supplier = form.supplier.data,
                        db_status=Asset.DB_status.E_ACTIVE,
                        description=form.description.data)
        db.session.add(asset)
        db.session.commit()
        flash('You have added asset {}'.format(asset.name))

        return redirect(url_for('asset.assets'))

    return render_template('asset/asset.html', form=form, title='Add')


#edit a asset
@asset.route('/asset/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    asset = Asset.query.get_or_404(id)
    form = EditForm(obj=asset)
    if form.validate_on_submit():
        if request.form['button'] == 'Save':
            form.populate_obj(asset)
            db.session.commit()
            flash('You have edited asset {}'.format(asset.name))

        return redirect(url_for('asset.assets'))

    return render_template('asset/asset.html', form=form, title='Edit')

#no login required
@asset.route('/asset/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    asset = Asset.query.get_or_404(id)
    form = ViewForm(obj=asset)
    if form.validate_on_submit():
        return redirect(url_for('asset.assets'))

    return render_template('asset/asset.html', form=form, title='View')


#no login required
@asset.route('/asset/qr/<string:qr>', methods=['GET', 'POST'])
def view_via_qr(qr):
    asset = Asset.query.filter_by(qr_code=qr).first_or_404()
    form = ViewForm(obj=asset)
    return render_template('asset/asset.html', form=form, title='View')

#delete an asset
@asset.route('/asset/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    flash('You have successfully deleted the asset.')

    return redirect(url_for('asset.assets'))

