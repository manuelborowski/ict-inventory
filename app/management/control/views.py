from flask import render_template, redirect, url_for, request, flash, send_file, session, make_response, jsonify
from flask_login import login_required, current_user

from .forms import AddForm, EditForm, ViewForm
from ... import db, log, user_plus_required
from . import control
from ...models import Asset, AssetLocation, Purchase, ControlCheckTemplate, ControlCardTemplate

from ...support import build_filter, get_ajax_table, get_setting_inc_index_asset_name
from ...tables_config import  tables_configuration
from ...documents import download_single_doc2

from io import StringIO
import csv, re, json

#This route is called by an ajax call on the assets-page to populate the table.
@control.route('/control/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['control'])

#show a list of assets
@control.route('/control', methods=['GET', 'POST'])
@login_required
@user_plus_required
def show():
    #The following line is required only to build the filter-fields on the page.
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['control'])
    return render_template('base_multiple_items.html',
                           title='Inspectie fiches',
                           filter=_filter, filter_form=_filter_form,
                           config = tables_configuration['control'],
                           )

@control.route('/control/add', methods=['GET', 'POST'])
@login_required
@user_plus_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            template = ControlCardTemplate(
                name=form.name.data,
                info=form.info.data,
                active=form.active.data,
                standards=form.standards.data
            )
            check_data = json.loads(request.form['check-data'])
            i = 0
            for check in check_data:
                if check['name'] == '': continue
                new_check = ControlCheckTemplate(index=i, name=check['name'], active=check['active'],
                                                 is_check=check['is_check'], template=template)
                db.session.add(new_check)
                i += 1
            db.session.commit()
        return redirect(url_for('management.control.show'))

    return render_template('management/control/control.html', form=form, title='Nieuwe inspectie fiche',
                           role='add', subject='management.control', route='management.control.show')


@control.route('/control/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def edit(id):
    template = ControlCardTemplate.query.get_or_404(id)
    form = EditForm(obj=template)
    if form.validate_on_submit():
        if request.form['button'] == 'Bewaar':
            form.populate_obj(template)
            check_data = json.loads(request.form['check-data'])
            check_cache = {c.index: c for c in template.checks}
            for check in check_data:
                index = int(check['index'])
                if index in check_cache:
                    check_cache[index].active = check['active']
                    check_cache[index].is_check = check['is_check']
                    check_cache[index].name = check['name']
                elif index == -1 and check['name'] != '':
                    new_index = len(check_cache)
                    new_check = ControlCheckTemplate(index=new_index, name=check['name'], active=check['active'],
                                                     is_check=check['is_check'], template=template)
                    db.session.add(new_check)
                    check_cache[new_index] = new_check
            db.session.commit()
        return redirect(url_for('management.control.show'))

    check_data = [{
        'index': c.index,
        'name': c.name,
        'is_check': c.is_check,
        'active': c.active
    } for c in template.checks]

    return render_template('management/control/control.html', form=form, title='Wijzig een inspectie fiche',
                           role='edit', subject='management.control', route='management.control.show',
                           check_data=check_data)


@control.route('/control/view/<int:id>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def view(id):
    template = ControlCardTemplate.query.get_or_404(id)
    form = ViewForm(obj=template)

    check_data = [{
        'index': c.index,
        'name': c.name,
        'is_check': c.is_check,
        'active': c.active
    } for c in template.checks]

    return render_template('management/control/control.html', form=form, title='Bekijk een inspectie fiche',
                           role='view', subject='management.control', route='management.control.show',
                           check_data=check_data)
