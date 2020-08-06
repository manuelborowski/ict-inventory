from flask import request, redirect, jsonify
from . import base
from ..documents import download_single_document, upload_documents
from urllib.parse import unquote

@base.route('/base/download/<string:document>/<string:file>', methods=['GET', 'POST'])
def download(document, file):
    return download_single_document(document,file)


@base.route('/base/upload/<string:document>/<string:url>', methods=['GET', 'POST'])
def upload(document, url):
    file_list = request.files.getlist('file_list')
    upload_documents(document, file_list)
    return redirect(unquote(url))

@base.route('/base/upload_ajax', methods=['POST'])
def upload_ajax():
    file_list = request.files.getlist('file_list')
    document_type = request.form['document-type']
    upload_documents(document_type, file_list)
    return jsonify({'status': True})


