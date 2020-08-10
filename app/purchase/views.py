# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db, log
from ..documents import upload_doc
from . import purchase
from ..models import Purchase

from ..support import build_filter, get_ajax_table
from ..tables_config import  tables_configuration
import os
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS

#This route is called by an ajax call on the assets-page to populate the table.
@purchase.route('/purchase/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['purchase'])

#ashow a list of purchases
@purchase.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchases():
    #The following line is required only to build the filter-fields on the page.
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['purchase'])
    return render_template('base_multiple_items.html',
                           title='aankopen',
                           filter=_filter, filter_form=_filter_form,
                           config=tables_configuration['purchase'])


#add a new purchase
@purchase.route('/purchase/add/<int:id>', methods=['GET', 'POST'])
@purchase.route('/purchase/add', methods=['GET', 'POST'])
@login_required
def add(id=-1):
    if id > -1:
        purchase = Purchase.query.get_or_404(int(id))
        form = AddForm(obj=purchase)
    else:
        form = AddForm()
    #Validate on the second pass only (when button 'Bewaar' is pushed)
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        purchase = Purchase(
            invoice=form.invoice.data,
            since=form.since.data,
            value=form.value.data,
            supplier = form.supplier.data,
            device = form.device.data)
        db.session.add(purchase)
        db.session.commit()
        log.info('add: {}'.format(purchase.log()))
        #flash(_(u'You have added purchase {}').format(purchase.since))
        return redirect(url_for('purchase.purchases'))

    return render_template('purchase/purchase.html', form=form, title='Voeg een aankoop toe', role='add', route='purchase.purchases',
                           subject='purchase')


#edit a purchase
@purchase.route('/purchase/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    purchase = Purchase.query.get_or_404(id)
    form = EditForm(obj=purchase)
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(purchase)
            try:
                upload_doc(request)
            except Exception as e:
                flash('Could not import file')
            db.session.commit()
            log.info('edit : {}'.format(purchase.log()))
            #flash(_(u'You have edited purchase {}').format(purchase))

        return redirect(url_for('purchase.purchases'))
    return render_template('purchase/purchase.html', form=form, title='Pas een aankoop aan', role='edit', route='purchase.purchases',
                           subject='purchase')


#no login required
@purchase.route('/purchase/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    purchase = Purchase.query.get_or_404(id)
    form = ViewForm(obj=purchase)
    if form.validate_on_submit():
        return redirect(url_for('purchase.purchases'))

    return render_template('purchase/purchase.html', form=form, title='Bekijk een aankoop', role='view', route='purchase.purchases', subject='purchase')

#delete a purchase
@purchase.route('/purchase/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    purchase = Purchase.query.get_or_404(id)
    log.info('delete: {}'.format(purchase.log()))
    db.session.delete(purchase)
    db.session.commit()
    #flash(_('You have successfully deleted the purchase.'))

    return redirect(url_for('purchase.purchases'))
