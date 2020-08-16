from flask import request, redirect, jsonify
from flask_login import login_required
from . import base
from ..documents import download_single_document, upload_documents, get_doc_list
from ..models import Device
from .. import user_plus_required
from urllib.parse import unquote
import json

@base.route('/base/download/<string:document>/<string:file>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def download(document, file):
    return download_single_document(document, file)


@base.route('/base/upload/<string:document>/<string:url>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def upload(document, url):
    file_list = request.files.getlist('file_list')
    upload_documents(document, file_list)
    return redirect(unquote(url))

@base.route('/base/upload_ajax', methods=['POST'])
@login_required
@user_plus_required
def upload_ajax():
    try:
        file_list = request.files.getlist('file_list')
        document_type = request.form['document-type']
        upload_documents(document_type, file_list)
        return jsonify({'status': True})
    except Exception as e:
        return jsonify({'status': False, 'details': repr(e)})
    return jsonify({'status': False, 'details': 'onbekede fout in upload_ajax'})


@base.route('/base/ajax_request/<string:jds>', methods=['GET', 'POST'])
@login_required
@user_plus_required
def ajax_request(jds):
    try:
        jd = json.loads(jds)
        if jd['action'] == 'get-document-options':
            document = jd['document']
            data = {
                'options': list(zip([''] + get_doc_list(document), [''] + get_doc_list(document))),
                'opaque': jd['opaque'],
            }
            return jsonify({"status": True, "data": data})
    except Exception as e:
        return jsonify({"status": False, 'details': f'{e}'})
    return jsonify({"status": False, 'details': f'Er is iets fout gegaan met action: {jd["action"]}\n{jds}'})

