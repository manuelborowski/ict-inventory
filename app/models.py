# -*- coding: utf-8 -*-
# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from sqlalchemy import UniqueConstraint

class User(UserMixin, db.Model):
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, unique=True)
    username = db.Column(db.String(256), index=True, unique=True)
    first_name = db.Column(db.String(256), index=True)
    last_name = db.Column(db.String(256), index=True)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    settings = db.relationship('Settings', cascade='all, delete-orphan', backref='user', lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('Paswoord kan je niet lezen.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def ret_dict(self):
        return {'id':self.id, 'email':self.email, 'username':self.username, 'first_name':self.first_name, 'last_name':self.last_name,
                'is_admin': self.is_admin}

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Asset(db.Model):
    __tablename__ = 'assets'

    class Status:
        E_IN_SERVICE = 'IN BEDRIJF'
        E_IN_REPAIR = 'IN REPARATIE'
        E_BROKEN = 'STUK'
        E_TO_BE_REPLACED = 'TE VERVANGEN'
        E_TOO_OLD = 'TE OUD'
        E_OTHER = 'ANDERS'
        DEFAULT = E_IN_SERVICE

        @staticmethod
        def get_list():
            l = [getattr(Asset.Status, a) for a in dir(Asset.Status) if a.startswith('E_')]
            l.remove(Asset.Status.DEFAULT)
            l.insert(0, Asset.Status.DEFAULT)
            return l

        @staticmethod
        def get_list_with_empty():
            l = Asset.Status.get_list()
            l.insert(0, '')
            return l

    class DB_status:
        E_NEW = 'NEW'
        E_ACTIVE = 'ACTIVE'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))        # eg PC245
    qr_code = db.Column(db.String(256), unique=True)
    status = db.Column(db.String(256))    # one of: IN_DIENST, HERSTELLING, STUK, TE_VERVANGEN, ANDERE
    location = db.Column(db.String(256))    # eg E203
    db_status = db.Column(db.String(256))    # one of: NIEW, ACTIEF, ANDERE
    serial = db.Column(db.String(256))      # serial number
    description = db.Column(db.String(256))
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'))

    def __repr__(self):
        return '<Asset: {}>'.format(self.name)

    def ret_dict(self):
        return {'id':self.id, 'name':self.name, 'qr_code':self.qr_code, 'status':self.status, 'location':self.location,
                'db_status':self.db_status,  'serial':self.serial, 'description':self.description,'purchase':self.purchase.ret_dict()}


class Purchase(db.Model):
    __tablename__= 'purchases'

    @staticmethod
    def reverse_date(date):
        return '-'.join(date.split('-')[::-1])

    id = db.Column(db.Integer, primary_key=True)
    since = db.Column(db.Date)
    value = db.Column(db.Numeric(20,2))      # e.g. 12.12
    commissioning = db.Column(db.String(256))    # path to commissioning document on disk
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    assets = db.relationship('Asset', cascade='all, delete-orphan', backref='purchase', lazy='dynamic')


    def __repr__(self):
        return '{} / {}'.format(self.since, self.value)

    def ret_dict(self):
        return {'id':self.id, 'since':self.since.strftime('%d-%m-%Y'), 'value':float(self.value), 'commissioning':self.commissioning,
                'supplier': self.supplier.ret_dict(), 'device':self.device.ret_dict()}

class Device(db.Model):
    __tablename__ = 'devices'

    class Category:
        @staticmethod
        def get_list():
            #l = [i.category for i in db.session.query(Device.category).distinct(Device.category).order_by(Device.category).all()]
            l = [
                'BEAMER',
                'PC',
                'MONITOR',
                'PRINTER',
                'GEREEDSCHAP',
                'KOPIEERAPPARAAT',
                'TV',
                'HUISHOUD',
                'ANDERE'
            ]
            return l

        @staticmethod
        def get_list_with_empty():
            l = Device.Category.get_list()
            l.insert(0, '')
            return l

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(256))       # the brand of the device
    type = db.Column(db.String(256))        # the type of the device
    category = db.Column(db.String(256))    # one of: PC, BEAMER, PRINTER, ANDERE
    power = db.Column(db.Numeric(20,1))      # e.g. 12.1
    photo = db.Column(db.String(256))    # path to photo on disk
    risk_analysis = db.Column(db.String(256))    # path to risk analysis document on disk
    manual = db.Column(db.String(256))    # path to manual document on disk
    safety_information = db.Column(db.String(256))    # path to safety information document on disk
    ce = db.Column(db.Boolean, default=False)       # conform CE regulations
    purchases = db.relationship('Purchase', cascade='all, delete-orphan', backref='device', lazy='dynamic')

    def __repr__(self):
        return '{} / {}'.format(self.brand, self.type)

    def ret_dict(self):
        return {'id':self.id, 'brand':self.brand, 'type':self.type, 'category':self.category, 'power':float(self.power), 'photo':self.photo,
        'risk_analysis': self.risk_analysis, 'manual':self.manual, 'safety_information':self.safety_information, 'ce':self.ce,
        'brandtype':self.brand + ' / ' + self.type}

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(1024))
    purchases = db.relationship('Purchase', cascade='all, delete-orphan', backref='supplier', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

    def ret_dict(self):
        return {'id':self.id, 'name':self.name, 'description':self.description}

class Settings(db.Model):
    __tablename__ = 'settings'

    class SETTING_TYPE:
        E_INT = 'INT'
        E_STRING = 'STRING'
        E_FLOAT = 'FLOAT'
        E_BOOL = 'BOOL'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    value = db.Column(db.String(256))
    type = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    UniqueConstraint('name', 'user_id')

    def __repr__(self):
        return '{}/{}/{}'.format(self.name, self.value, self.type)
