# -*- coding: utf-8 -*-
# app/supplier/__init__.py

from flask import Blueprint

supplier = Blueprint('supplier', __name__)

from . import views