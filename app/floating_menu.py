from .models import User

fmi_edit = {"menu_id": "edit_menu_item", "menu_text": "Wijzig", "route": "edit", "flags": ["id_required"]}
fmi_delete = {"menu_id": "delete_menu_item", "menu_text": "Verwijder", "route": "delete","flags": ["id_required", "confirm_before_delete"]}
fmi_copy = {"menu_id": "copy_menu_item", "menu_text": "Kopieer van", "route": "add", "flags": ["id_required"]}
fmi_add = {"menu_id": "add_menu_item", "menu_text": "Voeg toe", "route": "add", "flags": []}
fmi_view = {"menu_id": "view_menu_item", "menu_text": "Details", "route": "view", "flags": ["id_required"]}
fmi_change_password = {"menu_id": "change_password_menu_item", "menu_text": "Verander paswoord", "route": "change_password","flags": ["id_required"]}
fmi_add_inspection = {"menu_id": "add_inspection_menu_item", "menu_text": "Inspectie toevoegen", "route": "add_inspection", "flags": ["id_required"]}
fmi_inspection_overview = {"menu_id": "inspection_overview_menu_item", "menu_text": "Overzicht inspecties", "route": "inspection_overview", "flags": ["id_required"]}


default_menu = {
    User.LEVEL.USER: [fmi_view],
    User.LEVEL.USER_PLUS: [fmi_edit, fmi_copy, fmi_add, fmi_view, fmi_delete],
    User.LEVEL.ADMIN: [fmi_edit, fmi_copy, fmi_add, fmi_view, fmi_delete],
}

user_menu = {
    User.LEVEL.USER: [fmi_view],
    User.LEVEL.USER_PLUS: [fmi_edit, fmi_change_password],
    User.LEVEL.ADMIN: [fmi_edit, fmi_copy, fmi_add, fmi_view, fmi_delete, fmi_change_password],
}

no_delete_menu = {
    User.LEVEL.USER: [fmi_view],
    User.LEVEL.USER_PLUS: [fmi_edit, fmi_copy, fmi_add, fmi_view],
    User.LEVEL.ADMIN: [fmi_edit, fmi_copy, fmi_add, fmi_view],
}

asset_menu = {
    User.LEVEL.USER: [fmi_view],
    User.LEVEL.USER_PLUS: [fmi_edit, fmi_copy, fmi_add, fmi_view, fmi_delete, fmi_add_inspection, fmi_inspection_overview],
    User.LEVEL.ADMIN: [fmi_edit, fmi_copy, fmi_add, fmi_view, fmi_delete, fmi_add_inspection, fmi_inspection_overview],
}

inspect_menu = {
    User.LEVEL.USER: [fmi_view],
    User.LEVEL.USER_PLUS: [fmi_edit, fmi_view],
    User.LEVEL.ADMIN: [fmi_edit, fmi_view],
}

