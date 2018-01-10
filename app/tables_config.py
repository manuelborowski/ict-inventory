# -*- coding: utf-8 -*-

from models import Asset, Purchase, Device, Supplier

tables_configuration = {
    'asset' : {
        'model' : Asset,
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
        'view_route': 'asset.view',
        # 'href' : [{'attribute':'name', 'route':'asset.view', 'id':'id'},
        #           {'attribute':'purchase][supplier][name', 'route':'supplier.view', 'id':'id'}
        #           ]
        'href': [{'attribute': '["name"]', 'route': '"asset.view"', 'id': '["id"]'},
                 {'attribute': '["purchase"]["supplier"]["name"]', 'route': '"supplier.view"', 'id': '["purchase"]["supplier"]["id"]'},
                 {'attribute': '["purchase"]["device"]["brandtype"]', 'route': '"device.view"', 'id': '["purchase"]["device"]["id"]'}
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
        'view_route' : 'purchase.view',
        'href': [{'attribute': 'value', 'route': 'purchase.view', 'id': 'id'}]
}
}
