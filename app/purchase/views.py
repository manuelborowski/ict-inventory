# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, redirect, url_for, request, send_file, send_from_directory, config, flash
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db, _, app
from ..documents import get_doc_reference, get_doc_path, get_doc_list
from ..documents import document_type_list, get_doc_filename, get_doc_select, get_doc_download, get_doc_delete
from . import purchase
from ..models import Purchase

from ..base import build_filter, get_ajax_table
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
            try:
                for d in document_type_list:
                    if get_doc_filename(d) in request.files:
                        if request.files[get_doc_filename(d)]:
                            for f in request.files.getlist(get_doc_filename(d)):
                                filename = get_doc_reference(d).save(f)
            except Exception as e:
                flash('Could not import file')

            # try:
            #     if request.files['commissioning_filename']:
            #         filename = commissioning_docs.save(request.files['commissioning_filename'])
            # except Exception as e:
            #     flash('Cannot upload file, maybe wrong type', 'error')
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

#download a commissioning file
@purchase.route('/purchase/download/<string:file>', methods=['GET', 'POST'])
@login_required
def download(file=""):
    try:
        return send_file(os.path.join(app.root_path, '..', get_doc_path('commissioning'), file), as_attachment=True)
        #return app.send_static_file(os.path.join(commissioning_path, file))
    except Exception as e:
        flash(_('Could not download file {}'.format(file)))
        flash(_('Does it still exist?'))

    return redirect(url_for('purchase.purchases'))
