# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

settings = Blueprint('management.settings', __name__)

from . import views