from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required

from .forms import AddForm, EditForm, ViewForm
from .. import db, log, admin_required, user_plus_required
from ..documents import upload_doc
from . import invoice
from ..models import Invoice, DeviceCategory, Device, Purchase
from ..documents import get_doc_list

from ..support import build_filter, get_ajax_table
from ..tables_config import  tables_configuration
import os, json
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS

@invoice.route('/invoice/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['invoice'])

@invoice.route('/invoice', methods=['GET', 'POST'])
@login_required
def invoices():
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['invoice'])
    return render_template('base_multiple_items.html', title='facturen',
                           filter=_filter, filter_form=_filter_form,
                           config=tables_configuration['invoice'])


@invoice.route('/invoice/add/<int:id>', methods=['GET', 'POST'])
@invoice.route('/invoice/add', methods=['GET', 'POST'])
@login_required
@user_plus_required
def add(id=-1):
    if id > -1:
        invoice = Invoice.query.get_or_404(int(id))
        form = AddForm(obj=invoice)
        purchase_data = []
        for purchase in invoice.purchases:
            purchase_data.append({
                'id': purchase.id,
                'value': float(purchase.value),
                'category_id': purchase.device.category_id,
                'device_id': purchase.device.id,
                'commissioning': purchase.commissioning
            })
    else:
        form = AddForm()
        purchase_data = []
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        invoice = Invoice(
            number=form.number.data,
            since=form.since.data,
            info=form.info.data,
            supplier = form.supplier.data)
        db.session.add(invoice)
        purchase_data = json.loads(request.form['purchase-data'])
        for purchase in purchase_data:
            if purchase['device'] != '':
                try:
                    new_purchase = Purchase(
                        invoice=invoice,
                        value=float(purchase['value'].replace('.', '').replace(',', '.')),
                        device_id=int(purchase['device']),
                        commissioning=purchase['commissioning']
                    )
                    db.session.add(new_purchase)
                except Exception:
                    pass
        db.session.commit()
        log.info('add: {}'.format(invoice.log()))
        return redirect(url_for('invoice.invoices'))
    select_list = {
        'category': DeviceCategory.get_list_for_select_first_empty(),
        'commissioning': list(zip([''] + get_doc_list('commissioning'), [''] + get_doc_list('commissioning'))),
        'device': Device.get_list_for_select_first_empty()
    }
    return render_template('invoice/invoice.html', form=form, title='Voeg een factuur toe', role='add',
                           route='invoice.invoices', subject='invoice', select_list=select_list,
                           purchase_data=purchase_data)


@invoice.route('/invoice/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def edit(id):
    invoice = Invoice.query.get_or_404(id)
    form = EditForm(obj=invoice)
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(invoice)
            purchase_data = json.loads(request.form['purchase-data'])
            for purchase in purchase_data:
                if int(purchase['purchase-id']) != -1:
                    update_purchase = Purchase.query.get(int(purchase['purchase-id']))
                    update_purchase.value = float(purchase['value'].replace('.', '').replace(',', '.')),
                    update_purchase.device_id = int(purchase['device']),
                    update_purchase.commissioning = purchase['commissioning']
                elif int(purchase['device']) != -1:
                    try:
                        new_purchase = Purchase(
                            invoice=invoice,
                            value=float(purchase['value'].replace(',', '.')),
                            device_id=int(purchase['device']),
                            commissioning=purchase['commissioning']
                        )
                        db.session.add(new_purchase)
                    except Exception:
                        pass
            db.session.commit()
            log.info('edit : {}'.format(invoice.log()))
        return redirect(url_for('invoice.invoices'))
    select_list = {
        'category': DeviceCategory.get_list_for_select_first_empty(),
        'commissioning': list(zip([''] + get_doc_list('commissioning'), [''] + get_doc_list('commissioning'))),
        'device': Device.get_list_for_select_first_empty()
    }
    purchase_data = []
    for purchase in invoice.purchases:
        purchase_data.append({
            'id': purchase.id,
            'value': str(float(purchase.value)).replace('.', ','),
            'category_id': purchase.device.category_id,
            'device_id': purchase.device.id,
            'commissioning': purchase.commissioning
        })
    return render_template('invoice/invoice.html', form=form, title='Wijzig een factuur', role='edit',
                           route='invoice.invoices', subject='invoice', select_list=select_list,
                           purchase_data=purchase_data)


@invoice.route('/invoice/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    invoice = Invoice.query.get_or_404(id)
    form = ViewForm(obj=invoice)
    if form.validate_on_submit():
        return redirect(url_for('invoice.invoices'))

    select_list = {
        'category': DeviceCategory.get_list_for_select_first_empty(),
        'commissioning': list(zip([''] + get_doc_list('commissioning'), [''] + get_doc_list('commissioning'))),
        'device': Device.get_list_for_select_first_empty()
    }
    purchase_data = []
    for purchase in invoice.purchases:
        purchase_data.append({
            'id': purchase.id,
            'value': str(float(purchase.value)).replace('.', ','),
            'category_id': purchase.device.category_id,
            'device_id': purchase.device.id,
            'commissioning': purchase.commissioning
        })
    return render_template('invoice/invoice.html', form=form, title='Bekijk een factuur', role='view',
                           route='invoice.invoices', subject='invoice', select_list=select_list,
                           purchase_data=purchase_data)

@invoice.route('/invoice/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def delete(id):
    invoice = Invoice.query.get_or_404(id)
    log.info('delete: {}'.format(invoice.log()))
    db.session.delete(invoice)
    db.session.commit()
    return redirect(url_for('invoice.invoices'))

@invoice.route('/invoice/item_ajax/<string:jds>', methods=['GET', 'POST'])
@login_required
def item_ajax(jds):
    try:
        jd = json.loads(jds)
        if jd['action'] == 'category-changed':
            data = {
                'device_options': Device.get_list_for_select_first_empty(int(jd['category-id'])),
                'opaque_element_id': jd['opaque-element-id'],
            }
            return jsonify({"status": True, "data": data})
    except Exception as e:
        return jsonify({"status": False, 'details': f'{e}'})
    return jsonify({"status": False, 'details': f'Er is iets fout gegaan met action: {jd["action"]}\n{jds}'})


@invoice.route('/invoice/add_asset/<int:purchase_id>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def add_asset(purchase_id):
    return redirect(url_for('asset.add', id=-1, qr=-1, purchase_id=purchase_id))
