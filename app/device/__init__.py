# -*- coding: utf-8 -*-
# app/home/__init__.py

from flask import Blueprint

device = Blueprint('device', __name__)

from . import views