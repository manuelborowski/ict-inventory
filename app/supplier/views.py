# -*- coding: utf-8 -*-
# app/user/views.py

from flask import render_template, redirect, url_for, request
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db
from . import supplier
from ..models import Supplier

from ..base import build_filter, get_ajax_table
from ..tables_config import  tables_configuration

#This route is called by an ajax call on the assets-page to populate the table.
@supplier.route('/supplier/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['supplier'])

#ashow a list of suppliers
@supplier.route('/supplier', methods=['GET', 'POST'])
@login_required
def suppliers():
    #The following line is required only to build the filter-fields on the page.
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['supplier'])
    return render_template('base_multiple_items.html',
                           title='leveranciers',
                           filter=_filter, filter_form=_filter_form,
                           config = tables_configuration['supplier'])


#add a new supplier
@supplier.route('/supplier/add/<int:id>', methods=['GET', 'POST'])
@supplier.route('/supplier/add', methods=['GET', 'POST'])
@login_required
def add(id=-1):
    if id > -1:
        supplier = Supplier.query.get_or_404(int(id))
        form = AddForm(obj=supplier)
    else:
        form = AddForm()
    del form.id # is not required here and makes validate_on_submit fail...
    #Validate on the second pass only (when button 'Bewaar' is pushed)
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        supplier = Supplier(name=form.name.data,
                        description=form.description.data)
        db.session.add(supplier)
        db.session.commit()
        #flash('You have added supplier {}'.format(supplier.name))

        return redirect(url_for('supplier.suppliers'))

    return render_template('supplier/supplier.html', form=form, title='Voeg een leverancier toe', role='add', subject='supplier', route='supplier.suppliers')
#return render_template('device/device.html', form=form, title='Voeg een toestel toe', role='add', subject='device', route='device.devices')

#edit a supplier
@supplier.route('/supplier/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    supplier = Supplier.query.get_or_404(id)
    form = EditForm(obj=supplier)
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(supplier)
            db.session.commit()
            #flash('You have edited supplier {}'.format(supplier.name))

        return redirect(url_for('supplier.suppliers'))

    return render_template('supplier/supplier.html', form=form, title='Pas een leverancier aan', role='edit', subject='supplier', route='supplier.suppliers')

#no login required
@supplier.route('/supplier/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    supplier = Supplier.query.get_or_404(id)
    form = ViewForm(obj=supplier)
    if form.validate_on_submit():
        return redirect(url_for('supplier.suppliers'))

    return render_template('supplier/supplier.html', form=form, title='Bekijk een leverancier', role='view', subject='supplier', route='supplier.suppliers')


#delete a supplier
@supplier.route('/supplier/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    #flash('You have successfully deleted the supplier.')

    return redirect(url_for('supplier.suppliers'))

