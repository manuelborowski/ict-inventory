# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, render_template_string, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user
from flask_table import Table, Col, DateCol, LinkCol

import datetime, time

from .forms import AddForm, EditForm, ViewForm
from .. import db, _
from . import purchase
from ..models import Purchase
from ..views import NoEscapeCol

class PurchaseTable(Table):

    since = DateCol(_(u'Since'), date_format='dd-MM-YYYY')
    value = Col(_(u'Value'))      # value in euro
    supplier = LinkCol(_(u'Supplier'), 'supplier.edit', attr='supplier', url_kwargs=dict(id='supplier_id'))
    device = LinkCol(_(u'Device'), 'device.edit', attr='device', url_kwargs=dict(id='device_id'))
    delete = NoEscapeCol('')
    edit = NoEscapeCol('')
    view = NoEscapeCol('')
    id = Col('Id')
    copy_from = NoEscapeCol('C')
    classes = ['table ' 'table-striped ' 'table-bordered ']
    html_attrs = {'id': 'purchasetable', 'cellspacing': '0', 'width': '100%'}


def check_date_in_form(date_key, form):
    if date_key in form and form[date_key] != '':
        try:
            time.strptime(form[date_key], '%d-%M-%Y')
            return form[date_key]
        except:
            flash(_(u'Wrong date format, must be of form d-m-y'))
    return None

def check_value_in_form(value_key, form):
    if value_key in form and form[value_key] != '':
        try:
            float(form[value_key])
            return form[value_key]
        except:
            flash(_(u'Wrong value format'))
    return None

@purchase.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchases():
    purchases = Purchase.query.all()
    for p in purchases:
        p.copy_from = render_template_string("<input type='radio' name='copy_from' value='" + str(p.id) + "'>")
        p.delete = render_template_string("<a class='confirmBeforeDelete' u_id=" + str(p.id) + "><i class='fa fa-trash'></i></a>")
        p.edit = render_template_string("<a href=\"{{ url_for('purchase.edit', id=" + str(p.id) + ") }}\"><i class='fa fa-pencil'></i>")
        p.view = render_template_string("<a href=\"{{ url_for('purchase.view', id=" + str(p.id) + ") }}\"><i class='fa fa-eye'></i>")
    purchase_table = PurchaseTable(purchases)

    return render_template('purchase/purchases.html', title='purchases', route='purchase.purchases', subject='purchase', table=purchase_table, filter=filter)


#add a new purchase
@purchase.route('/purchase/add', methods=['GET', 'POST'])
@login_required
def add():
    if 'copy_from' in request.form:
        purchase = Purchase.query.get_or_404(int(request.form['copy_from']))
        form = AddForm(obj=purchase)
    else:
        form = AddForm()
    del form.id # is not required here and makes validate_on_submit fail...
    if not 'add' in request.form and form.validate_on_submit():
        purchase = Purchase(since=form.name.since,
                            value=form.value.data,
                           supplier = form.supplier.data,
                           device = form.device.data)
        db.session.add(purchase)
        db.session.commit()
        flash(_(u'You have added purchase {}').format(purchase.since))
        return redirect(url_for('purchase.purchases'))

    return render_template('purchase/purchase.html', form=form, title=_(u'Add a purchase'), role='add', route='purchase.purchases', subject='purchase')


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
            flash(_(u'You have edited purchase {}').format(format.since))

        return redirect(url_for('purchase.purchases'))

    return render_template('purchase/purchase.html', form=form, title=_(u'Edit a purchase'), role='edit', route='purchase.purchases', subject='purchase')

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
    flash(_('You have successfully deleted the purchase.'))

    return redirect(url_for('purchase.purchases'))

