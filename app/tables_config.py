# -*- coding: utf-8 -*-

from models import Asset, Purchase, Device, Supplier, User

floating_menu_config = {
    "edit" : {"menu_id" : "edit_menu_item", "menu_text": "Edit", "route" : "edit", "flags" : ["id_required"]},
    "delete" : {"menu_id" : "delete_menu_item", "menu_text": "Delete", "route": "delete", "flags": ["id_required", "confirm_before_delete"]},
    "copy": {"menu_id": "copy_menu_item", "menu_text": "Copy from", "route": "add", "flags": ["id_required"]},
    "add": {"menu_id": "add_menu_item", "menu_text": "Add", "route": "add", "flags": []},
    "view": {"menu_id": "view_menu_item", "menu_text": "View", "route": "view", "flags": ["id_required"]},
}


tables_configuration = {
    'asset' : {
        'model' : Asset,
        'title' : 'assets',
        'route' : 'asset.assets',
        'subject' :'asset',
        'delete_message' : '',
        'template' : [{'name': 'Name', 'data':'name', 'order_by': Asset.name},
                      {'name': 'Category', 'data':'purchase.device.category', 'order_by': Device.category},
                      {'name': 'Location', 'data':'location', 'order_by': Asset.location},
                      {'name': 'Since', 'data':'purchase.since', 'order_by': Purchase.since},
                      {'name': 'Value', 'data':'purchase.value', 'order_by': Purchase.value},
                      {'name': 'QR', 'data':'qr_code', 'order_by': Asset.qr_code},
                      {'name': 'Status', 'data':'status', 'order_by': Asset.status},
                      {'name': 'Supplier', 'data':'purchase.supplier.name', 'order_by': Supplier.name},
                      {'name': 'Device', 'data':'purchase.device.brandtype', 'order_by': Device.brand},
                      {'name': 'Serial', 'data': 'serial', 'order_by': Asset.serial}],
        'filter' :  ['since', 'value', 'location', 'category', 'status', 'supplier', 'device'],
        'href': [{'attribute': '["name"]', 'route': '"asset.view"', 'id': '["id"]'},
                 {'attribute': '["purchase"]["since"]', 'route': '"purchase.view"', 'id': '["purchase"]["id"]'},
                 {'attribute': '["purchase"]["supplier"]["name"]', 'route': '"supplier.view"', 'id': '["purchase"]["supplier"]["id"]'},
                 {'attribute': '["purchase"]["device"]["brandtype"]', 'route': '"device.view"', 'id': '["purchase"]["device"]["id"]'}
                 ],
        'floating_menu' : [ floating_menu_config['edit'],
                            floating_menu_config['copy'],
                            floating_menu_config['add'],
                            floating_menu_config['view'],
                            floating_menu_config['delete'],
                          ]
    },
    'purchase' : {
        'model' : Purchase,
        'template' : [
            {'name': 'Value', 'data': 'value', 'order_by': Purchase.value},
            {'name': 'Since', 'data': 'since', 'order_by': Purchase.since},
            {'name': 'Supplier', 'data': 'supplier.name', 'order_by': Supplier.name},
            {'name': 'Device', 'data': 'device.brandtype', 'order_by':Device.brand}],
        'filter' :  ['since', 'value', 'supplier', 'device'],
        'href': [{'attribute': '["value"]', 'route': '"purchase.view"', 'id': '["id"]'},
                 {'attribute': '["supplier"]["name"]', 'route': '"supplier.view"', 'id': '["supplier"]["id"]'},
                 {'attribute': '["device"]["brandtype"]', 'route': '"device.view"', 'id': '["device"]["id"]'}
                ],
        'floating_menu': [floating_menu_config['edit'],
                          floating_menu_config['copy'],
                          floating_menu_config['add'],
                          floating_menu_config['view'],
                          floating_menu_config['delete'],
                          ]
    },
    'device': {
        'model': Device,
        'template': [
            {'name': 'Brand', 'data': 'brand', 'order_by': Device.brand},
            {'name': 'Type', 'data': 'type', 'order_by': Device.type},
            {'name': 'Category', 'data': 'category', 'order_by': Device.category},
            {'name': 'CE', 'data': 'ce', 'order_by': Device.ce},
            {'name': 'Power', 'data': 'power', 'order_by': Device.power}],
        'filter': ['category', 'device'],
        'href': [{'attribute': '["brand"]', 'route': '"device.view"', 'id': '["id"]'},
                 ],
        'floating_menu': [floating_menu_config['edit'],
                          floating_menu_config['copy'],
                          floating_menu_config['add'],
                          floating_menu_config['view'],
                          floating_menu_config['delete'],
                          ]
    },
    'supplier': {
        'model': Supplier,
        'template': [
            {'name': 'Name', 'data': 'name', 'order_by': Supplier.name},
            {'name': 'Description', 'data' : 'description', 'order_by': Supplier.description}],
        'filter': ['supplier'],
        'href': [{'attribute': '["name"]', 'route': '"supplier.view"', 'id': '["id"]'},
                 ],
        'floating_menu': [floating_menu_config['edit'],
                          floating_menu_config['copy'],
                          floating_menu_config['add'],
                          floating_menu_config['view'],
                          floating_menu_config['delete'],
                          ]
    },
    'user': {
        'model': User,
        'template': [
            {'name': 'Username', 'data': 'username', 'order_by': User.username},
            {'name': 'First name', 'data': 'first_name', 'order_by': User.first_name},
            {'name': 'Last name', 'data': 'last_name', 'order_by': User.last_name},
            {'name': 'Email', 'data': 'email', 'order_by': User.email},
            {'name': 'Is admin', 'data': 'is_admin', 'order_by': User.is_admin},],
        'filter': [],
        'href': [{'attribute': '["username"]', 'route': '"user.view"', 'id': '["id"]'},
                 ],
        'floating_menu': [floating_menu_config['edit'],
                          floating_menu_config['copy'],
                          floating_menu_config['add'],
                          floating_menu_config['view'],
                          floating_menu_config['delete'],
                          ]
    }
}

