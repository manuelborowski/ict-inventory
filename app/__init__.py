# -*- coding: utf-8 -*-

# app/__init__.py

# third-party imports
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_jsglue import JSGlue
from werkzeug.routing import IntegerConverter as OrigIntegerConvertor
import config, logging, logging.handlers, os, sys
from functools import wraps

app = Flask(__name__, instance_relative_config=True)

# V1.0 : reworked to python V3.7.2
# V1.1 : small bugfixes and updates
# V1.2 : python 2 to 3 : zip() to list(zip())
# V2.0 : update to nginx
# V2.1 : small bugfix
# V2.2 : introduced 3-levels for users, added invoice-field, assets are counted per purchase, assetvalue is added
# V2.3 : added purchase_id in assets-view
# V2.4 : settings are visible only by at least user+
# V2.5 : moved users, settings and documents under management
# V2.6 : added table DeviceCategory
# V2/7 : use table DeviceCategory throughout the program
# V2.8 : added table AssetLocation
# V2.9 : fixed github security errors
# V2.10 : use table AssetLocation throughout de code
# V2.11 : added table Invoice and functionality to support it
# V2.12 : processing table : clean up
# V2.13 : invoice is working
# V2.14 : cleanup in floating menu
# V2.15 : added functionality for easier navigating between topics
# V2.16 : imort control cards from excel and load into database
# V2.17 : a device can have a control card
# V2.18 : add, edit, view control card templates
# V2.19 : check-lines can be moved up and down
# V2.20 : clean up of several topics, added inspect topic
# V2.21 : added overview of inspections per asset
# V3.0 : introduce invoices and inspections
# V3.1 : included database functions in models
# V3.2 : default user initialization
# V3.3 : update of topic devices
# V3.4 : cleanup of item forms
# V3.5 : added ControlCardLevel table and updated inspections
# V3.6 : clean up in html/css. Added inspection functionality
# V3.7 : make tables leaner
# V3.8 : update in requirements.txt
# V3.9 : bugfixed issue with floating menu.  Improved handling of currency numbers (1.234,45).  Bugfixed copy-from-asset
# V3.10 : bugfix location_id when copying from an asset
# V3.11 : bugfix issue with location
# V3.12 : bugfix issue with location, part 2
# V3.13 : bugfix : invoice date changed to today.  Device category was wrong
# V3.14 : bugfix : it is not possible to use a dot as separator in currency
# V3.15 : bugfix : adding a new device
# V3.16 : when copying from existing asset with trailing index number, take number of leading zero's into account
# V3.17 : update invoice : skip non-valid entries
# V3.18: bugfix in change password
# V3.19: upgrade nginx

@app.context_processor
def inject_version():
    return dict(version = 'V3.19')


#enable logging
LOG_HANDLE = 'IAI'
log = logging.getLogger(LOG_HANDLE)

# local imports
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()

#The original werkzeug-url-converter cannot handle negative integers (e.g. asset/add/-1/1)  
class IntegerConverter(OrigIntegerConvertor):
    regex = r'-?\d+'
    num_convert = int

config_name = os.getenv('FLASK_CONFIG')
config_name = config_name if config_name else 'production'

def create_admin(db):
    from app.models import User
    admin = User.query.filter(User.username == 'admin')
    if not admin:
        admin = User(username='admin', password='admin', is_admin=True)
        db.session.add(admin)
        db.session.commit()


# support custom filtering while logging
class MyLogFilter(logging.Filter):
    def filter(self, record):
        record.username = current_user.username if current_user and current_user.is_active else 'NONE'
        return True


# set up logging
LOG_FILENAME = os.path.join(sys.path[0], app_config[config_name].STATIC_PATH, 'log/iai-log.txt')
try:
    log_level = getattr(logging, app_config[config_name].LOG_LEVEL)
except:
    log_level = getattr(logging, 'INFO')
log.setLevel(log_level)
log.addFilter(MyLogFilter())
log_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10 * 1024, backupCount=5)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(username)s - %(message)s')
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)

log.info('start IAI')

app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')

Bootstrap(app)

jsglue = JSGlue(app)
db.app=app  # hack :-(
db.init_app(app)

app.url_map.converters['int'] = IntegerConverter

login_manager.init_app(app)
login_manager.login_message = 'Je moet aangemeld zijn om deze pagina te zien!'
login_manager.login_view = 'auth.login'

migrate = Migrate(app, db)

from app import models

if 'db' in sys.argv:
    from app import models
else:
    create_admin(db) # Only once

    #init default users level
    models.User.default_init()

    #init default supplier
    models.Supplier.default_init()

    #device categories are put in a separate table.
    models.DeviceCategory.default_init()
    models.Device.device_category_init()

    #asset location are put in a separate table
    models.AssetLocation.default_init()
    models.Asset.asset_location_init()

    #init default invoices
    models.Invoice.default_init()
    models.Purchase.invoice_init()

    #init control card templates
    models.ControlCardTemplate.default_init()
    models.Device.device_control_template_init()

    #init default asset quantity (1)
    models.Asset.default_init()

    #init default control card levels
    models.ControlCardLevel.default_init()

    #flask db migrate
    #flask db upgrade
    #uncheck when migrating database
    #return app

    def admin_required(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_at_least_admin:
                abort(403)
            return func(*args, **kwargs)

        return decorated_view


    # decorator to grant access to at least supervisors
    def user_plus_required(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_at_least_user_plus:
                abort(403)
            return func(*args, **kwargs)

        return decorated_view

    from .management.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .base import base as base_blueprint
    app.register_blueprint(base_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .management.user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .inspect import inspect as inspect_blueprint
    app.register_blueprint(inspect_blueprint)

    from .asset import asset as asset_blueprint
    app.register_blueprint(asset_blueprint)

    from .supplier import supplier as supplier_blueprint
    app.register_blueprint(supplier_blueprint)

    from .invoice import invoice as invoice_blueprint
    app.register_blueprint(invoice_blueprint)

    from .device import device as device_blueprint
    app.register_blueprint(device_blueprint)

    from .purchase import purchase as purchase_blueprint
    app.register_blueprint(purchase_blueprint)

    from .management.settings import settings as settings_blueprint
    app.register_blueprint(settings_blueprint)

    from .management.device_category import category as category_blueprint
    app.register_blueprint(category_blueprint)

    from .management.asset_location import location as location_blueprint
    app.register_blueprint(location_blueprint)

    from .management.control import control as control_blueprint
    app.register_blueprint(control_blueprint)

    from .documents import init_documents
    init_documents(app, 'commissioning')
    init_documents(app, 'risk_analysis')
    init_documents(app, 'photo')
    init_documents(app, 'manual')
    init_documents(app, 'safety_information')

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    @app.route('/500')
    def error_500():
        abort(500)

