#Collect all functionality with respect to uploading the different types of files

from flask_uploads import UploadSet, configure_uploads, ALL
import os

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
    documents_config[d]['full_path'] = os.path.join(app.config['STATIC_PATH'], doc_dest)
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
        print e
        return None

def get_doc_path(d):
    try:
        return documents_config[d]['full_path']
    except Exception as e:
        print e
        return None

def get_doc_list(d):
    file_list = sorted(os.listdir(get_doc_path(d)))
    return file_list if file_list else []

def upload_doc(request):
    for d in document_type_list:
        if get_doc_filename(d) in request.files and request.files[get_doc_filename(d)]:
            fl = get_doc_list(d)
            for f in request.files.getlist(get_doc_filename(d)):
                if not f.filename in fl:
                    filename = get_doc_reference(d).save(f, name=f.filename)
                    fl.append(f.filename)
