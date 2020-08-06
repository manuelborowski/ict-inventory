#Collect all functionality with respect to uploading the different types of files

from flask_uploads import UploadSet, configure_uploads, ALL
from flask import send_file
from . import app
import os, sys

document_type_list = [
    'photo',
    'commissioning',
    'risk_analysis',
    'manual',
    'safety_information'
]

documents_config = {}

def init_documents(app, d):
    documents_config[d] = {}
    doc_dest = d.replace('_', '')
    upload_dest = 'UPLOADED_' + doc_dest.upper() + '_DEST'
    documents_config[d]['full_path'] = os.path.join(sys.path[0], app.config['STATIC_PATH'], doc_dest)
    app.config[upload_dest] = documents_config[d]['full_path']
    documents_config[d]['doc_reference'] = UploadSet(doc_dest, ALL)
    configure_uploads(app, documents_config[d]['doc_reference'])

def get_doc_select(d):
    return d + '_select'

def get_doc_delete(d):
    return d + '_delete'

def get_doc_download(d):
    return d + '_download'

def get_doc_filename(d):
    return d + '_filename'

def get_doc_reference(d):
    try:
        return documents_config[d]['doc_reference']
    except Exception as e:
        return None

def get_doc_path(d):
    try:
        return documents_config[d]['full_path']
    except Exception as e:
        return None

def get_doc_list(d):
    file_list = sorted(os.listdir(get_doc_path(d)))
    filtered_list = list(filter(lambda x: x[0] != '.', file_list))
    return filtered_list if filtered_list else []


def upload_documents(document_type, file_list):
    fl = get_doc_list(document_type)
    for f in file_list:
        if not f.filename in fl:
            filename = get_doc_reference(document_type).save(f, name=f.filename)
            fl.append(f.filename)


def upload_doc(request):
    for d in document_type_list:
        if get_doc_filename(d) in request.files and request.files[get_doc_filename(d)]:
            fl = get_doc_list(d)
            for f in request.files.getlist(get_doc_filename(d)):
                if not f.filename in fl:
                    filename = get_doc_reference(d).save(f, name=f.filename)
                    fl.append(f.filename)


def download_single_document(document_type, file_name):
    try:
        return send_file(os.path.join(app.root_path, '..', get_doc_path(document_type), file_name), as_attachment=True)
    except Exception as e:
        pass
    return ('', 204)


def download_single_doc2(request):
    for d in document_type_list:
        if get_doc_download(d) in request.form and request.form[d]:
            return send_file(os.path.join(app.root_path, '..', get_doc_path(d), request.form[d]), as_attachment=True)
    return ('', 204)
