#Collect all functionality with respect to uploading the different types of files

from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, IMAGES, ALL
import os


############" COMMISSIONING ################
#the name of the uploadset is reused in UPLOADED_..._DEST
commissioning_path = 'commissioning'
commissioning_docs = UploadSet(commissioning_path, ALL)
commissioning_full_path = ''

def init_commissioning_documents(app):
    global commissioning_full_path
    commissioning_full_path = os.path.join(app.config['STATIC_PATH'], commissioning_path)
    app.config['UPLOADED_COMMISSIONING_DEST'] = commissioning_full_path
    configure_uploads(app, commissioning_docs)


def get_commissioning_docs():
    cms_file_list = [""] + sorted(os.listdir(commissioning_full_path))
    return cms_file_list if cms_file_list else []

############" RISK ANANLYSIS ################
risk_analysis_path = 'riskanalysis'
risk_analysis_docs = UploadSet(risk_analysis_path, ALL)
risk_analysis_full_path = ''

def init_risk_analysis_documents(app):
    global risk_analysis_full_path
    risk_analysis_full_path = os.path.join(app.config['STATIC_PATH'], risk_analysis_path)
    app.config['UPLOADED_RISKANALYSIS_DEST'] = risk_analysis_full_path
    configure_uploads(app, risk_analysis_docs)

def get_risk_analysis_docs():
    file_list = [""] + sorted(os.listdir(risk_analysis_full_path))
    return file_list if file_list else []

############" PHOTO ################
photo_path = 'photo'
photo_docs = UploadSet(photo_path, IMAGES)
photo_full_path = ''

def init_photo_documents(app):
    global photo_full_path
    photo_full_path = os.path.join(app.config['STATIC_PATH'], photo_path)
    app.config['UPLOADED_PHOTO_DEST'] = photo_full_path
    configure_uploads(app, photo_docs)

def get_photo_docs():
    file_list = [""] + sorted(os.listdir(photo_full_path))
    return file_list if file_list else []

############" MANUAL ################
manual_path = 'manual'
manual_docs = UploadSet(manual_path, ALL)
manual_full_path = ''

def init_manual_documents(app):
    global manual_full_path
    manual_full_path = os.path.join(app.config['STATIC_PATH'], manual_path)
    app.config['UPLOADED_MANUAL_DEST'] = manual_full_path
    configure_uploads(app, manual_docs)

def get_manual_docs():
    file_list = [""] + sorted(os.listdir(manual_full_path))
    return file_list if file_list else []

############" SAFETY INFORMATION ################
safety_information_path = 'safetyinformation'
safety_information_docs = UploadSet(safety_information_path, ALL)
safety_information_full_path = ''

def init_safety_information_documents(app):
    global safety_information_full_path
    safety_information_full_path = os.path.join(app.config['STATIC_PATH'], safety_information_path)
    app.config['UPLOADED_SAFETYINFORMATION_DEST'] = safety_information_full_path
    configure_uploads(app, safety_information_docs)

def get_safety_information_docs():
    file_list = [""] + sorted(os.listdir(safety_information_full_path))
    return file_list if file_list else []

