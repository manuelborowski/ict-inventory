# -*- coding: utf-8 -*-

from models import Asset, Purchase, Device, Supplier, User
import user.extra_filtering
from floating_menu import default_menu_config

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
        'floating_menu' : default_menu_config,
    },
    'purchase' : {
        'model' : Purchase,
        'title' : 'purchase',
        'route' : 'purchase.purchases',
        'subject' :'purchase',
        'delete_message' : 'Are you sure you want to delete this purchase AND all associated assets?',
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
        'floating_menu' : default_menu_config,
    },
    'device': {
        'model': Device,
        'title' : 'device',
        'route' : 'device.devices',
        'subject' :'device',
        'delete_message' : 'Are you sure you want to delete this device AND all associated purchases AND assets?',
        'template': [
            {'name': 'Brand', 'data': 'brand', 'order_by': Device.brand},
            {'name': 'Type', 'data': 'type', 'order_by': Device.type},
            {'name': 'Category', 'data': 'category', 'order_by': Device.category},
            {'name': 'CE', 'data': 'ce', 'order_by': Device.ce},
            {'name': 'Power', 'data': 'power', 'order_by': Device.power}],
        'filter': ['category', 'device'],
        'href': [{'attribute': '["brand"]', 'route': '"device.view"', 'id': '["id"]'},
                 ],
        'floating_menu' : default_menu_config,
    },
    'supplier': {
        'model': Supplier,
        'title' : 'supplier',
        'route' : 'supplier.suppliers',
        'subject' :'supplier',
        'delete_message' : 'Are you sure you want to delete this supplier AND all associated purchases AND assets?',
        'template': [
            {'name': 'Name', 'data': 'name', 'order_by': Supplier.name},
            {'name': 'Description', 'data' : 'description', 'order_by': Supplier.description}],
        'filter': ['supplier'],
        'href': [{'attribute': '["name"]', 'route': '"supplier.view"', 'id': '["id"]'},
                 ],
        'floating_menu' : default_menu_config,
    },
    'user': {
        'model': User,
        'title' : 'user',
        'route' : 'user.users',
        'subject' :'user',
        'delete_message' : '',
        'template': [
            {'name': 'Username', 'data': 'username', 'order_by': User.username},
            {'name': 'First name', 'data': 'first_name', 'order_by': User.first_name},
            {'name': 'Last name', 'data': 'last_name', 'order_by': User.last_name},
            {'name': 'Email', 'data': 'email', 'order_by': User.email},
            {'name': 'Is admin', 'data': 'is_admin', 'order_by': User.is_admin},],
        'filter': [],
        'href': [{'attribute': '["username"]', 'route': '"user.view"', 'id': '["id"]'},
                 ],
        'floating_menu' : default_menu_config,
        'query_filter' : user.extra_filtering.filter,
    }
}

