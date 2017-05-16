# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, render_template_string, flash, redirect, url_for, request
from flask_login import login_required
from flask_table import Table, Col, DateCol

import datetime

from .forms import AddForm, EditForm
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
    date_in_service = DateCol('Since')
    qr_code = Col('QR')
    category = Col('Category')    # one of: PC, BEAMER, PRINTER, ANDERE
    status = Col('Status')    # one of: IN_DIENST, HERSTELLING, STUK, TE_VERVANGEN, ANDERE
    value = Col('Value')      # 100 times value in eurocents
    location = Col('Location')    # eg E203
    picture = Col('Picture')    # path to picture on disk
    db_status = Col('DB status')    # one of: NIEW, ACTIEF, ANDERE
    description = Col('Description')
    #supplier_id = Col('Supplier')
    delete = NoEscapeCol('')
    edit = NoEscapeCol('')
    classes = ['table ' 'table-striped ' 'table-bordered ']
    html_attrs = {'id': 'usertable', 'cellspacing': '0', 'width': '100%'}


@asset.route('/asset', methods=['GET', 'POST'])
@login_required
def assets():
    assets = Asset.query.all()
    for a in assets:
        a.delete = render_template_string("<a class='confirmBeforeDelete' u_id=" + str(a.id) + "><i class='fa fa-trash'></i></a>")
        a.edit = render_template_string("<a href=\"{{ url_for('asset.edit', id=" + str(a.id) + ") }}\"><i class='fa fa-pencil'></i>")
    asset_table = AssetTable(assets)

    return render_template('asset/assets.html', title='assets', asset_table=asset_table, table_id='assettable')


#add a new asset
@asset.route('/asset/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        asset = Asset(name=form.name.data,
                        date_in_service=form.date_in_service.data,
                        qr_code=form.qr_code.data,
                        category=form.category.data,
                        status=form.status.data,
                        value=form.value.data * 100, #from cents to euro
                        location=form.location.data,
                        picture=form.picture.data,
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
    form.value.data = asset.value / 100;
    if form.validate_on_submit():
        if request.form['button'] == 'Save':
            form.populate_obj(asset)
            asset.value = form.value.data * 100;
            db.session.commit()
            flash('You have edited asset {}'.format(asset.name))

        return redirect(url_for('asset.assets'))

    return render_template('asset/asset.html', form=form, title='Edit')


#delete an asset
@asset.route('/asset/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    flash('You have successfully deleted the asset.')

    return redirect(url_for('asset.assets'))

