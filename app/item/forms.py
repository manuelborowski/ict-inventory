# -*- coding: utf-8 -*-
#app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department, Role


class DepartmentForm(FlaskForm):
    """
    Form for an administrator to add or edit a departement
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for an administrator to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(), get_label='name')
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label='name')
    submit = SubmitField('Submit')