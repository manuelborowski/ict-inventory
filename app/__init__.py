# -*- coding: utf-8 -*-

# app/__init__.py

# third-party imports
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_jsglue import JSGlue

# local imports
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_admin(db):
    from app.models import User
    admin = User(username='admin', password='admin', is_admin=True)
    db.session.add(admin)
    db.session.commit()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    Bootstrap(app)

    jsglue = JSGlue(app)

    db.app=app  # hack :-(
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access this page'
    login_manager.login_view = 'auth.login'

    migrate = Migrate(app, db)

    from app import models

    #create_admin(db) # Only once

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .supplier import supplier as supplier_blueprint
    app.register_blueprint(supplier_blueprint)

    from .asset import asset as asset_blueprint
    app.register_blueprint(asset_blueprint)

    #from .table import table as table_blueprint
    #app.register_blueprint(table_blueprint)

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

    return app