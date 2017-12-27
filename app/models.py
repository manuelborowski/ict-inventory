# -*- coding: utf-8 -*-
# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


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

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

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


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Asset(db.Model):
    __tablename__ = 'assets'

    class Status:
        E_IN_SERVICE = 'IN SERVICE'
        E_IN_REPAIR = 'IN REPAIR'
        E_BROKEN = 'BROKEN'
        E_TO_BE_REPLACED = 'TO BE REPLACED'
        E_OTHER = 'OTHER'
        DEFAULT = E_IN_SERVICE

        @staticmethod
        def get_list():
            l = [getattr(Asset.Status, a) for a in dir(Asset.Status) if a.startswith('E_')]
            l.remove(Asset.Status.DEFAULT)
            l.insert(0, Asset.Status.DEFAULT)
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
    assets = db.relationship('Asset', backref='purchase', lazy='dynamic')


    def __repr__(self):
        return '{} / {}'.format(self.since, self.value)

class Device(db.Model):
    __tablename__ = 'devices'

    class Category:
        E_PC = 'PC'
        E_BEAMER = 'BEAMER'
        E_PRINTER = 'PRINTER'
        E_OTHER = 'OTHER'
        DEFAULT = E_PC

        @staticmethod
        def get_list():
            l = [getattr(Device.Category, a) for a in dir(Device.Category) if a.startswith('E_')]
            l.remove(Device.Category.DEFAULT)
            l.insert(0, Device.Category.DEFAULT)
            return l

        @staticmethod
        def get_list_with_empty():
            l = [getattr(Device.Category, a) for a in dir(Device.Category) if a.startswith('E_')]
            #l.remove(Device.Category.DEFAULT)
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
    purchases = db.relationship('Purchase', backref='device', lazy='dynamic')

    def __repr__(self):
        return '{} / {}'.format(self.brand, self.type)

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(1024))
    purchases = db.relationship('Purchase', backref='supplier', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

