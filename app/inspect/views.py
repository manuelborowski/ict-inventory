from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user

from .forms import AddForm, EditForm, ViewForm
from .. import db, log, admin_required, user_plus_required
from ..documents import upload_doc
from . import inspect
from ..models import Asset, InspectCard, InspectCheck
from ..documents import get_doc_list

from ..support import build_filter, get_ajax_table
from ..tables_config import  tables_configuration
import os, json
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS

@inspect.route('/inspect/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['inspect'])

@inspect.route('/inspect', methods=['GET', 'POST'])
@login_required
def show():
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['inspect'])
    return render_template('base_multiple_items.html', title='Inspectie',
                           filter=_filter, filter_form=_filter_form,
                           config=tables_configuration['inspect'])


@inspect.route('/inspect/add/<int:id>', methods=['GET', 'POST'])
@inspect.route('/inspect/add', methods=['GET', 'POST'])
@login_required
@user_plus_required
def add(id=-1):
    form = AddForm()
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        asset = Asset.query.get(id)
        control_template = asset.purchase.device.control_template
        check_data = json.loads(request.form['check-data'])
        card = InspectCard(inspector=form.inspector.data,
                           date=form.date.data,
                           info=form.info.data,
                           active=form.active.data,
                           template=control_template,
                           asset=asset
        )
        for check in check_data:
            if check['is-check'] == 'false': continue
            new_check = InspectCheck(index=check['check-index'],
                                     remark=check['remark'],
                                     result=check['result'],
                                     card=card
            )
            db.session.add(new_check)
        db.session.add(card)
        db.session.commit()
    return redirect(url_for('asset.assets'))


@inspect.route('/inspect/add_from_asset/<int:asset_id>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def add_from_asset(asset_id=-1):
    asset = Asset.query.get(asset_id)
    control_template = asset.purchase.device.control_template
    check_cache = {c.index: c for c in control_template.checks}
    form = AddForm()
    form.id.data = asset_id
    form.inspector.data = f'{current_user.first_name} {current_user.last_name}'
    check_template_data = []
    for i in range(len(check_cache)):
        if not check_cache[i].active: continue
        check_template_data.append({
            'index': check_cache[i].index,
            'name': check_cache[i].name,
            'is_check': check_cache[i].is_check
        })

    return render_template('inspect/inspect.html', form=form, title='Voeg een inspectie toe', role='add',
                           route='inspect.show', subject='inspect',
                           check_template_data=check_template_data)


@inspect.route('/inspect/overview_from_asset/<int:asset_id>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def overview_from_asset(asset_id=-1):
    asset = Asset.query.get(asset_id)
    if not asset.inspections: return redirect (url_for('inspection.show'))
    all_checks_data = []
    for inspect in sorted(asset.inspections, key=lambda x: x.date):
        inspect_check_cache = {c.index: c for c in inspect.checks}
        template_check_cache = {c.index: c for c in inspect.template.checks}
        check_data = []
        for i in sorted(template_check_cache):
            if not template_check_cache[i].active: continue
            result = inspect_check_cache[i].result if template_check_cache[i].is_check else 'na'
            remark = inspect_check_cache[i].remark if template_check_cache[i].is_check else ''
            check_data.append({
                'is_check': template_check_cache[i].is_check,
                'result': result,
                'remark': remark,
            })
        date = inspect.date.strftime('%d-%m-%Y').replace('-', '<br>')
        all_checks_data.append({
            'date': date,
            'inspector': inspect.inspector,
            'info': inspect.info,
            'checks': check_data
        })
    template = asset.inspections[0].template
    inspection_items = [{
        'name': c.name,
        'is_check': c.is_check,
    } for c in sorted(template.checks, key=lambda x: x.index)]
    inspect_overview_data = {
        'asset': asset.name,
        'template_name': template.name,
        'template_standards': template.standards,
        'template_info': template.info,
        'template_items': inspection_items,
        'all_checks': all_checks_data
    }

    return render_template('inspect/inspection_overview.html', title='Overzicht inspecties', overview_data=inspect_overview_data)

@inspect.route('/inspect/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def edit(id):
    inspect = InspectCard.query.get_or_404(id)
    form = EditForm(obj=inspect)
    if 'button' in request.form and request.form['button'] == 'Bewaar' and form.validate_on_submit():
        form.populate_obj(inspect)
        check_cache = {c.index: c for c in inspect.checks}
        check_data = json.loads(request.form['check-data'])
        for check in check_data:
            if check['is-check'] == 'false': continue
            index = int(check['check-index'])
            check_cache[index].remark = check['remark']
            check_cache[index].result = check['result']
        db.session.commit()
        return redirect(url_for('inspect.show'))

    inspect_check_cache = {c.index: c for c in inspect.checks}
    template_check_cache = {c.index: c for c in inspect.template.checks}
    check_template_data = []
    for i in sorted(template_check_cache):
        if not template_check_cache[i].active: continue
        result = inspect_check_cache[i].result if template_check_cache[i].is_check else 'NVT'
        remark = inspect_check_cache[i].remark if template_check_cache[i].is_check else ''
        check_template_data.append({
            'index': i,
            'name': template_check_cache[i].name,
            'is_check': template_check_cache[i].is_check,
            'result': result,
            'remark': remark,
        })

    return render_template('inspect/inspect.html', form=form, title='Wijzig een inspectie', role='edit',
                           route='inspect.show', subject='inspect',
                           check_template_data=check_template_data)


@inspect.route('/inspect/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    inspect = InspectCard.query.get_or_404(id)
    form = ViewForm(obj=inspect)
    inspect_check_cache = {c.index: c for c in inspect.checks}
    template_check_cache = {c.index: c for c in inspect.template.checks}

    check_template_data = []
    for i in sorted(template_check_cache):
        if not template_check_cache[i].active: continue
        result = inspect_check_cache[i].result if template_check_cache[i].is_check else 'NVT'
        remark = inspect_check_cache[i].remark if template_check_cache[i].is_check else ''
        check_template_data.append({
            'index': i,
            'name': template_check_cache[i].name,
            'is_check': template_check_cache[i].is_check,
            'result': result,
            'remark': remark,
        })

    return render_template('inspect/inspect.html', form=form, title='Bekijk een inspectie', role='view',
                           route='inspect.show', subject='inspect',
                           check_template_data=check_template_data)



