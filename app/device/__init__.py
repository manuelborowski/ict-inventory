# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
import os

#the name of the uploadset is reused in UPLOADED_..._DEST
ra_path = 'riskanalysis'
ra_docs = UploadSet(ra_path, DOCUMENTS)
ra_full_path = ''

photo_path = 'photo'
photo_docs = UploadSet(photo_path, DOCUMENTS)
photo_full_path = ''

manual_path = 'manual'
manual_docs = UploadSet(manual_path, DOCUMENTS)
manual_full_path = ''

safety_information_path = 'safetyinformation'
safety_information_docs = UploadSet(safety_information_path, DOCUMENTS)
safety_information_full_path = ''


def init_documents(app):
    global ra_full_path
    global photo_full_path
    global manual_full_path
    global safety_information_full_path

    ra_full_path = os.path.join(app.config['STATIC_PATH'], ra_path)
    app.config['UPLOADED_RISKANALYSIS_DEST'] = ra_full_path
    configure_uploads(app, ra_docs)

    photo_full_path = os.path.join(app.config['STATIC_PATH'], photo_path)
    app.config['UPLOADED_PHOTO_DEST'] = photo_full_path
    configure_uploads(app, photo_docs)

    manual_full_path = os.path.join(app.config['STATIC_PATH'], manual_path)
    app.config['UPLOADED_MANUAL_DEST'] = manual_full_path
    configure_uploads(app, manual_docs)

    safety_information_full_path = os.path.join(app.config['STATIC_PATH'], safety_information_path)
    app.config['UPLOADED_SAFETYINFORMATION_DEST'] = safety_information_full_path
    configure_uploads(app, safety_information_docs)

def get_ra_docs():
    file_list = [""] + sorted(os.listdir(ra_full_path))
    return file_list if file_list else []

def get_photo_docs():
    file_list = [""] + sorted(os.listdir(photo_full_path))
    return file_list if file_list else []

def get_manual_docs():
    file_list = [""] + sorted(os.listdir(manual_full_path))
    return file_list if file_list else []

def get_safety_information_docs():
    file_list = [""] + sorted(os.listdir(safety_information_full_path))
    return file_list if file_list else []



from flask import Blueprint

device = Blueprint('device', __name__)

from . import views