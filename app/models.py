from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import column_property
from sqlalchemy.sql import func
import datetime

def boolean_to_dutch(value):
    return 'JA' if value else 'NEE'

class User(UserMixin, db.Model):
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    class LEVEL:
        USER = 1
        USER_PLUS = 3
        ADMIN = 5

        ls = ["GEBRUIKER", "GEBRUIKER+", "ADMINISTRATOR"]

        @staticmethod
        def i2s(i):
            if i == 1:
                return User.LEVEL.ls[0]
            elif i == 3:
                return User.LEVEL.ls[1]
            if i == 5:
                return User.LEVEL.ls[2]

    @staticmethod
    def get_zipped_levels():
        return list(zip(["1", "3", "5"], User.LEVEL.ls))


    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True)
    username = db.Column(db.String(256), index=True, unique=True)
    first_name = db.Column(db.String(256), index=True)
    last_name = db.Column(db.String(256), index=True)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    settings = db.relationship('Settings', cascade='all, delete', backref='user', lazy='dynamic')
    level = db.Column(db.Integer)

    @property
    def is_at_least_user(self):
        return self.level >= User.LEVEL.USER

    @property
    def is_strict_user(self):
        return self.level == User.LEVEL.USER

    @property
    def is_at_least_user_plus(self):
        return self.level >= User.LEVEL.USER_PLUS

    @property
    def is_at_least_admin(self):
        return self.level >= User.LEVEL.ADMIN

    @property
    def get_level(self):
        return self.level

    @property
    def password(self):
        raise AttributeError('Paswoord kan je niet lezen.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def log(self):
        return '<User: {}/{}>'.format(self.id, self.username)

    def ret_dict(self):
        return {'id':self.id, 'email':self.email, 'username':self.username, 'first_name':self.first_name, 'last_name':self.last_name,
                'is_admin': self.is_admin, 'level': User.LEVEL.i2s(self.level)}

    @staticmethod
    def default_init():
        user = User.query.first()
        if not user.level:
            users = User.query.all()
            for user in users:
                user.level = User.LEVEL.ADMIN
            db.session.commit()


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
    quantity = db.Column(db.Integer, default=1)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id', ondelete='CASCADE'))
    location_id = db.Column(db.Integer, db.ForeignKey('asset_locations.id', ondelete='CASCADE'))
    inspections = db.relationship('InspectCard', cascade='all, delete', backref='asset', lazy='joined')


    def __repr__(self):
        return '<Asset: {}>'.format(self.name)

    def log(self):
        return '<Asset: {}/{}/{}/{}/{}>'.format(self.id, self.name, self.qr_code, self.purchase.since, self.purchase.value)

    def ret_dict(self):
        return {'id':self.id, 'name':self.name, 'qr_code':self.qr_code, 'status':self.status,
                'location':self.location2.ret_dict(),
                'invoice_purchase': f'{self.purchase.invoice.number} ({self.purchase.id})',
                'db_status':self.db_status,  'serial':self.serial, 'description':self.description,
                'purchase':self.purchase.ret_dict(), 'quantity': self.quantity}

    @staticmethod
    def asset_location_init():
        asset = Asset.query.first()
        if not asset.location_id:
            locations = {l.name: l.id for l in AssetLocation.query.all()}
            assets = Asset.query.all()
            for asset in assets:
                asset.location_id = locations[asset.location]
            db.session.commit()

    @staticmethod
    def default_init():
        asset = Asset.query.first()
        if not asset.quantity:
            assets = Asset.query.all()
            for asset in assets:
                asset.quantity = 1
            db.session.commit()


class AssetLocation(db.Model):
    __tablename__ = 'asset_locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    info = db.Column(db.String(1024), default='')
    active = db.Column(db.Boolean, default=True)
    assets = db.relationship('Asset', cascade='all, delete', backref='location2', lazy='dynamic')

    def __repr__(self):
        return f'<AssetLocation: {self.name}/{self.active}>'

    def ret_dict(self):
        return {'id':self.id, 'name':self.name, 'info': self.info, 'active': boolean_to_dutch(self.active)}

    @staticmethod
    def get_list_for_select(active=True):
        locations = AssetLocation.query
        if active is not None:
            locations = locations.filter(AssetLocation.active == active)
        locations = locations.order_by(AssetLocation.name).all()
        choices = [[l.id, l.name] for l in locations]
        return choices


    @staticmethod
    def get_list_for_select_first_empty():
        choices = AssetLocation.get_list_for_select(active=None)
        choices.insert(0, ['', ''])
        return choices

    @staticmethod
    def default_init():
        location_found = Asset.query.filter(Asset.location_id != None).first()
        if not location_found:
            locations = db.session.query(Asset.location).distinct(Asset.location).all()
            for location in locations:
                new_location = AssetLocation(name=location[0])
                db.session.add(new_location)
            db.session.commit()
        unknown_location = AssetLocation.query.filter(AssetLocation.name == 'ONBEKEND').first()
        if not unknown_location:
            unknown_location = AssetLocation(name='ONBEKEND', info='standaard locatie')
            db.session.add(unknown_location)
            db.session.commit()


class Purchase(db.Model):
    __tablename__= 'purchases'

    @staticmethod
    def reverse_date(date):
        return '-'.join(date.split('-')[::-1])

    id = db.Column(db.Integer, primary_key=True)
    since = db.Column(db.Date)
    value = db.Column(db.Numeric(20,2))      # e.g. 12.12
    commissioning = db.Column(db.String(256))    # path to commissioning document on disk
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id', ondelete='CASCADE'))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id', ondelete='CASCADE'))
    assets = db.relationship('Asset', cascade='all, delete', backref='purchase', lazy='dynamic')
    nbr_assets = column_property(func.nbr_assets(id))
    asset_value = column_property(func.asset_value(id))

    def __repr__(self):
        return f'{self.invoice.number}/{self.device.brand}/{self.device.type}'

    def log(self):
        return f'<Purchase: {self.id}, {self.value}, {self.device.brand}, {self.device.type}'

    def ret_dict(self):
        return {'id':self.id, 'value':str(float(self.value)).replace('.', ','),
                'commissioning':self.commissioning, 'device':self.device.ret_dict(), 'invoice': self.invoice.ret_dict(),
                'asset_value': str(float(self.asset_value if self.asset_value else 0)).replace('.', ','),
                'nbr_assets': self.nbr_assets if self.nbr_assets else 0}


    @staticmethod
    def invoice_init():
        purchase = Purchase.query.first()
        if not purchase.invoice_id:
            invoice = Invoice.query.filter(Invoice.number == 'ONBEKEND').first()
            purchases = Purchase.query.all()
            for purchase in purchases:
                purchase.invoice = invoice
            db.session.commit()


class Invoice(db.Model):
    __tablename__= 'invoices'

    @staticmethod
    def reverse_date(date):
        return '-'.join(date.split('-')[::-1])

    id = db.Column(db.Integer, primary_key=True)
    since = db.Column(db.Date)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'))
    number = db.Column(db.String(256), default='')    # invoice reference
    info = db.Column(db.String(1024), default='')
    purchases = db.relationship('Purchase', cascade='all, delete', backref='invoice', lazy='dynamic')
    # nbr_assets = column_property(func.nbr_assets(id))
    # asset_value = column_property(func.asset_value(id))

    def __repr__(self):
        return f'{self.number}/{self.since}/'

    def log(self):
        return f'<Invoice: {self.id}/{self.since}/{self.number}>'

    def ret_dict(self):
        return {'id':self.id, 'since':self.since.strftime('%d-%m-%Y'), 'number': self.number,
                'supplier':self.supplier.ret_dict(), 'info': self.info}

    @staticmethod
    def default_init():
        default = Invoice.query.filter(Invoice.number == 'ONBEKEND').all()
        if not default:
            default_supplier = Supplier.query.filter(Supplier.name == 'ONBEKEND').first()
            default = Invoice(number='ONBEKEND',
                              info='standaard factuur wanneer echte factuur niet gekend is',
                              since=datetime.datetime.now(),
                              supplier=default_supplier)
            db.session.add(default)
            db.session.commit()


class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(256))       # the brand of the device
    type = db.Column(db.String(256))        # the type of the device
    category = db.Column(db.String(256))    # one of: PC, BEAMER, PRINTER, ANDERE
    category_id = db.Column(db.Integer, db.ForeignKey('device_categories.id', ondelete='CASCADE'))
    power = db.Column(db.Numeric(20,1))      # e.g. 12.1
    photo = db.Column(db.String(256))    # path to photo on disk
    risk_analysis = db.Column(db.String(256))    # path to risk analysis document on disk
    manual = db.Column(db.String(256))    # path to manual document on disk
    safety_information = db.Column(db.String(256))    # path to safety information document on disk
    ce = db.Column(db.Boolean, default=False)       # conform CE regulations
    purchases = db.relationship('Purchase', cascade='all, delete', backref='device', lazy='dynamic')
    control_template_id = db.Column(db.Integer, db.ForeignKey('control_card_templates.id'))

    def __repr__(self):
        return '{}/{}'.format(self.brand, self.type)

    def log(self):
        return '<Device: {}/{}/{}>'.format(self.id, self.brand, self.type)

    def ret_dict(self):
        return {'id':self.id, 'brand':self.brand, 'type':self.type, 'category':self.category2.ret_dict(), 'power':float(self.power), 'photo':self.photo,
        'risk_analysis': self.risk_analysis, 'manual':self.manual, 'safety_information':self.safety_information, 'ce':self.ce,
        'brandtype':self.brand + ' / ' + self.type , 'control_template': self.control_template.ret_dict()}

    @staticmethod
    def device_category_init():
        device = Device.query.first()
        if not device.category_id:
            categories = {c.name: c.id for c in DeviceCategory.query.all()}
            devices = Device.query.all()
            for device in devices:
                device.category_id = categories[device.category]
            db.session.commit()

    @staticmethod
    def get_list_for_select(filter_category_id=None):
        devices = Device.query
        if filter_category_id:
            devices = devices.filter(Device.category_id == filter_category_id)
        devices = devices.order_by(Device.brand, Device.type).all()
        options = [[d.id, f'{d.brand}/{d.type}'] for d in devices]
        return options

    @staticmethod
    def get_list_for_select_first_empty(filter_category_id=None):
        options = Device.get_list_for_select(filter_category_id)
        options.insert(0, ['', ''])
        return options

    @staticmethod
    def device_control_template_init():
        device = Device.query.first()
        if not device.control_template_id:
            template = ControlCardTemplate.query.filter(ControlCardTemplate.name=='NVT').first()
            for device in Device.query.all():
                device.control_template = template
            db.session.commit()


class DeviceCategory(db.Model):
    __tablename__ = 'device_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    info = db.Column(db.String(1024), default='')
    active = db.Column(db.Boolean, default=True)
    devices = db.relationship('Device', cascade='all, delete', backref='category2', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}/{self.active}'

    def ret_dict(self):
        return {'id':self.id, 'name':self.name, 'info':self.info, 'active':boolean_to_dutch(self.active)}

    @staticmethod
    def get_list_for_select(active=True):
        categories = DeviceCategory.query
        if active is not None:
            categories = categories.filter(DeviceCategory.active == active)
        categories = categories.order_by(DeviceCategory.name).all()
        choices = [[c.id, c.name] for c in categories]
        return choices

    @staticmethod
    def get_list_for_select_first_empty():
        choices = DeviceCategory.get_list_for_select(active=None)
        choices.insert(0, ['', ''])
        return choices

    @staticmethod
    def default_init():
        default = ['BEAMER', 'PC', 'MONITOR', 'PRINTER', 'GEREEDSCHAP', 'KOPIEERAPPARAAT', 'TV', 'HUISHOUD', 'ANDERE']
        beamer = DeviceCategory.query.filter(DeviceCategory.name == 'BEAMER').first()
        if not beamer:
            for name in default:
                category = DeviceCategory(name=name)
                db.session.add(category)
            db.session.commit()


class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    description = db.Column(db.String(1024))
    purchases = db.relationship('Purchase', cascade='all, delete', backref='supplier', lazy='dynamic')
    invoices = db.relationship('Invoice', cascade='all, delete', backref='supplier', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

    def log(self):
        return '<Supplier: {}/{}>'.format(self.id, self.name)

    def ret_dict(self):
        return {'id':self.id, 'name':self.name, 'description':self.description}

    @staticmethod
    def default_init():
        default = Supplier.query.filter(Supplier.name == 'ONBEKEND').all()
        if not default:
            default = Supplier(name='ONBEKEND',
                              description='standaard leverancier wanneer echte leverancier niet gekend is')
            db.session.add(default)
            db.session.commit()


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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    UniqueConstraint('name', 'user_id')

    def log(self):
        return '<Setting: {}/{}/{}/{}>'.format(self.id, self.name, self.value, self.type)


class ControlCardTemplate(db.Model):
    __tablename__ = 'control_card_templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    info = db.Column(db.String(1024), default='')
    active = db.Column(db.Boolean, default=True)
    nlevels = db.Column(db.Integer, default=4)
    checks = db.relationship('ControlCheckTemplate', cascade='all, delete', backref='template', lazy='dynamic')
    standards = db.Column(db.String(1024), default='')
    devices = db.relationship('Device', backref='control_template', lazy='dynamic')
    inspect_cards = db.relationship('InspectCard', backref='template', lazy='dynamic')

    def __repr__(self):
        return f'{self.name}'

    def ret_dict(self):
        return {'id':self.id, 'name':self.name, 'active': boolean_to_dutch(self.active), 'info': self.info, 'standards': self.standards}

    @staticmethod
    def get_list_for_select(active=True):
        templates = ControlCardTemplate.query
        if active is not None:
            templates = templates.filter(ControlCardTemplate.active == active)
        templates = templates.order_by(ControlCardTemplate.name).all()
        choices = [[l.id, l.name] for l in templates]
        return choices

    @staticmethod
    def get_all(active=None):
        templates = ControlCardTemplate.query
        if active:
            templates = templates.filter(ControlCardTemplate.active==active)
        templates = templates.order_by(ControlCardTemplate.name).all()
        return templates

    @staticmethod
    def get_default():
        return ControlCardTemplate.default_init()

    @staticmethod
    def get_list_for_select_first_empty():
        templates = ControlCardTemplate.get_list_for_select(active=None)
        templates.insert(0, ['', ''])
        return templates

    @staticmethod
    def default_init():
        template = ControlCardTemplate.query.filter(ControlCardTemplate.name == 'NVT').first()
        if not template:
            template = ControlCardTemplate(name='NVT', info='Er is geen controle fiche voor dit toestel')
            db.session.add(template)
            db.session.commit()
        return template

    @staticmethod
    def level_to_color(level):
        if level == 4: return 'green'
        elif level == 3: return 'yellow'
        elif level == 2: return 'orange'
        elif level == 1: return 'red'
        return 'red'


class ControlCardLevel(db.Model):
    __tablename__ = 'control_card_levels'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    info = db.Column(db.String(256))
    color = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'{self.level}/{self.info}/{self.active}'

    default_levels = [
        [4, 'green', 'OK'],
        [3, 'yellow', 'ERNST C  eenvoudige herstelling'],
        [2, 'orange', 'ERNST B  dringend, risicovol'],
        [1, 'red', 'ERNST A ernstig onmiddellijk ingrijpen']
    ]

    @staticmethod
    def default_init():
        level = ControlCardLevel.query.first()
        if not level:
            for default in ControlCardLevel.default_levels:
                level = ControlCardLevel(
                    level = default[0],
                    color = default[1],
                    info = default[2]
                )
                db.session.add(level)
            db.session.commit()



class ControlCheckTemplate(db.Model):
    __tablename__ = 'control_check_templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    index = db.Column(db.Integer)
    is_check = db.Column(db.Boolean, default=True)
    active = db.Column(db.Boolean, default=True)
    template_id = db.Column(db.Integer, db.ForeignKey('control_card_templates.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<ControlCheck: {self.name}/{self.index}/{self.is_check}/{self.active}>'

    def ret_dict(self):
        return {'id':self.id, 'name':self.name}


class InspectCard(db.Model):
    __tablename__ = 'inspect_cards'

    id = db.Column(db.Integer, primary_key=True)
    inspector = db.Column(db.String(256))
    date = db.Column(db.Date)
    info = db.Column(db.String(1024), default='')
    active = db.Column(db.Boolean, default=True)
    card_template_id = db.Column(db.Integer, db.ForeignKey('control_card_templates.id', ondelete='CASCADE'))
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    checks = db.relationship('InspectCheck', cascade='all, delete', backref='card', lazy='dynamic')

    def __repr__(self):
        return f'{self.inspector}/{self.date}'

    def ret_dict(self):
        return {'id': self.id, 'inspector':self.inspector, 'date': self.date.strftime('%d-%m-%Y'),
                'active': boolean_to_dutch(self.active), 'info': self.info, 'template': self.template.ret_dict(),
                'asset': self.asset.ret_dict()}

class InspectCheck(db.Model):
    __tablename__ = 'inspect_checks'

    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Integer, default=1)
    remark = db.Column(db.String(256), default='')
    index = db.Column(db.Integer)
    card_id = db.Column(db.Integer, db.ForeignKey('inspect_cards.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'{self.result}/{self.index}/{self.remark}'

    def ret_dict(self):
        return {'id':self.id, 'result': self.result, 'index': self.index, 'remark': self.remark,
                'color': ControlCardTemplate.level_to_color(self.result)}


# database functions
# CREATE DEFINER=`root`@`localhost` FUNCTION `asset_value`(id int) RETURNS decimal(10,2)
# BEGIN
# 	DECLARE nbr decimal(10, 2);
#     DECLARE purchase_value decimal(10, 2);
#     select sum(assets.quantity) into nbr
#     from purchases
# 	join assets on assets.purchase_id = purchases.id
# 	where purchases.id = id;
#     select purchases.value into purchase_value
#     from purchases
# 	where purchases.id = id;
#     return purchase_value / nbr;
# END
#
#
# CREATE DEFINER=`root`@`localhost` FUNCTION `nbr_assets`(id int) RETURNS int(11)
# BEGIN
# 	DECLARE nbr INT;
#     select sum(assets.quantity) into nbr
#     from purchases
# 	join assets on assets.purchase_id = purchases.id
# 	where purchases.id = id;
#     return nbr;
# END