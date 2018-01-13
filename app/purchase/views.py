# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, redirect, url_for, request
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db, _
from . import purchase
from ..models import Purchase

from ..base import build_filter, get_ajax_table
from ..tables_config import  tables_configuration

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
                           title='purchases',
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
    del form.id # is not required here and makes validate_on_submit fail...
    if not 'add' in request.form and form.validate_on_submit():
        purchase = Purchase(since=form.since.data,
                            value=form.value.data,
                           supplier = form.supplier.data,
                           device = form.device.data)
        db.session.add(purchase)
        db.session.commit()
        #flash(_(u'You have added purchase {}').format(purchase.since))
        return redirect(url_for('purchase.purchases'))

    return render_template('purchase/purchase.html', form=form, title=_(u'Add a purchase'), role='add', route='purchase.purchases',
                           subject='purchase')


#edit a purchase
@purchase.route('/purchase/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    purchase = Purchase.query.get_or_404(id)
    form = EditForm(obj=purchase)
    if form.validate_on_submit():
        if request.form['button'] == _(u'Save'):
            form.populate_obj(purchase)
            db.session.commit()
            #flash(_(u'You have edited purchase {}').format(purchase))

        return redirect(url_for('purchase.purchases'))

    return render_template('purchase/purchase.html', form=form, title=_(u'Edit a purchase'), role='edit', route='purchase.purchases',
                           subject='purchase')

#no login required
@purchase.route('/purchase/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    purchase = Purchase.query.get_or_404(id)
    form = ViewForm(obj=purchase)
    if form.validate_on_submit():
        return redirect(url_for('purchase.purchases'))

    return render_template('purchase/purchase.html', form=form, title=_(u'View a purchase'), role='view', route='purchase.purchases', subject='purchase')

#delete a purchase
@purchase.route('/purchase/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    purchase = Purchase.query.get_or_404(id)
    db.session.delete(purchase)
    db.session.commit()
     #flash(_('You have successfully deleted the purchase.'))

    return redirect(url_for('purchase.purchases'))

