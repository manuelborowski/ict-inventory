# -*- coding: utf-8 -*-

fmi_edit = {"menu_id": "edit_menu_item", "menu_text": "Edit", "route": "edit", "flags": ["id_required"]}
fmi_delete = {"menu_id": "delete_menu_item", "menu_text": "Delete", "route": "delete","flags": ["id_required", "confirm_before_delete"]}
fmi_copy = {"menu_id": "copy_menu_item", "menu_text": "Copy from", "route": "add", "flags": ["id_required"]}
fmi_add = {"menu_id": "add_menu_item", "menu_text": "Add", "route": "add", "flags": []}
fmi_view = {"menu_id": "view_menu_item", "menu_text": "View", "route": "view", "flags": ["id_required"]}
fmi_change_pwd = {"menu_id": "view_menu_item", "menu_text": "Change password", "route": "view","flags": ["id_required"]}

default_menu_config = [
    fmi_edit,
    fmi_copy,
    fmi_add,
    fmi_view,
    fmi_delete
]

user_menu_config = [
    fmi_edit,
    fmi_change_pwd
]

admin_menu_config = [
    fmi_edit,
    fmi_copy,
    fmi_add,
    fmi_view,
    fmi_delete,
    fmi_change_pwd
]