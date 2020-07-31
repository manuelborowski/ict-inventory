from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db, log
from ..documents import upload_doc
from . import invoice
from ..models import Invoice

from ..base import build_filter, get_ajax_table
from ..tables_config import  tables_configuration
import os
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS

#This route is called by an ajax call on the assets-page to populate the table.
@invoice.route('/invoice/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['invoice'])

@invoice.route('/invoice', methods=['GET', 'POST'])
@login_required
def invoices():
    #The following line is required only to build the filter-fields on the page.
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['invoice'])
    return render_template('base_multiple_items.html',
                           title='facturen',
                           filter=_filter, filter_form=_filter_form,
                           config=tables_configuration['invoice'])


@invoice.route('/invoice/add/<int:id>', methods=['GET', 'POST'])
@invoice.route('/invoice/add', methods=['GET', 'POST'])
@login_required
def add(id=-1):
    if id > -1:
        invoice = Invoice.query.get_or_404(int(id))
        form = AddForm(obj=invoice)
    else:
        form = AddForm()
    del form.id # is not required here and makes validate_on_submit fail...
    #Validate on the second pass only (when button 'Bewaar' is pushed)
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        invoice = Invoice(
            number=form.number.data,
            since=form.since.data,
            supplier_id = form.supplier.data)
        db.session.add(invoice)
        db.session.commit()
        log.info('add: {}'.format(invoice.log()))
        #flash(_(u'You have added invoice {}').format(invoice.since))
        return redirect(url_for('invoice.invoices'))

    return render_template('invoice/invoice.html', form=form, title='Voeg een factuur toe', role='add',
                           route='invoice.invoices', subject='invoice')


#edit a invoice
@invoice.route('/invoice/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    invoice = Invoice.query.get_or_404(id)
    form = EditForm(obj=invoice)
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(invoice)
            try:
                upload_doc(request)
            except Exception as e:
                flash('Could not import file')
            db.session.commit()
            log.info('edit : {}'.format(invoice.log()))
            #flash(_(u'You have edited invoice {}').format(invoice))

        return redirect(url_for('invoice.invoices'))
    return render_template('invoice/invoice.html', form=form, title='Pas een aankoop aan', role='edit', route='invoice.invoices',
                           subject='invoice')


#no login required
@invoice.route('/invoice/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    invoice = Invoice.query.get_or_404(id)
    form = ViewForm(obj=invoice)
    if form.validate_on_submit():
        return redirect(url_for('invoice.invoices'))

    return render_template('invoice/invoice.html', form=form, title='Bekijk een aankoop', role='view', route='invoice.invoices', subject='invoice')

#delete a invoice
@invoice.route('/invoice/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    invoice = Invoice.query.get_or_404(id)
    log.info('delete: {}'.format(invoice.log()))
    db.session.delete(invoice)
    db.session.commit()
    #flash(_('You have successfully deleted the invoice.'))

    return redirect(url_for('invoice.invoices'))
