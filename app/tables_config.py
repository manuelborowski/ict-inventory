from .models import Asset, Purchase, Device, Supplier, User, DeviceCategory
from .management.user.extra_filtering import filter
from .floating_menu import default_menu_config, edit_add_view_menu_config

tables_configuration = {
    'asset' : {
        'model' : Asset,
        'title' : 'activa',
        'subject' :'asset',
        'delete_message' : '',
        'template' : [
            {'name': 'Naam', 'data':'name', 'order_by': Asset.name},
            {'name': '#', 'data':'quantity', 'order_by': Asset.quantity},
            {'name': 'Factuur', 'data':'purchase.invoice', 'order_by': Purchase.invoice},
            {'name': 'Categorie', 'data':'purchase.device.category', 'order_by': Device.category},
            {'name': 'Locatie', 'data':'location', 'order_by': Asset.location},
            {'name': 'Datum', 'data':'purchase.since', 'order_by': Purchase.since},
            {'name': 'Bedrag', 'data':'purchase.asset_value', 'order_by': Purchase.asset_value},
            {'name': 'QR', 'data':'qr_code', 'order_by': Asset.qr_code},
            {'name': 'Status', 'data':'status', 'order_by': Asset.status},
            {'name': 'Leverancier', 'data':'purchase.supplier.name', 'order_by': Supplier.name},
            {'name': 'Toestel', 'data':'purchase.device.brandtype', 'order_by': Device.brand},
            {'name': 'SerieNr', 'data': 'serial', 'order_by': Asset.serial}],
        'filter' :  ['since', 'value', 'invoice', 'location', 'category', 'status', 'supplier', 'device', 'purchase_id'],
        'href': [{'attribute': '["name"]', 'route': '"asset.view"', 'id': '["id"]'},
                 {'attribute': '["purchase"]["invoice"]', 'route': '"purchase.view"', 'id': '["purchase"]["id"]'},
                 {'attribute': '["purchase"]["since"]', 'route': '"purchase.view"', 'id': '["purchase"]["id"]'},
                 {'attribute': '["purchase"]["supplier"]["name"]', 'route': '"supplier.view"', 'id': '["purchase"]["supplier"]["id"]'},
                 {'attribute': '["purchase"]["device"]["brandtype"]', 'route': '"device.view"', 'id': '["purchase"]["device"]["id"]'}
                 ],
        'floating_menu' : default_menu_config,
        'export' : 'asset.exportcsv',
    },
    'purchase' : {
        'model' : Purchase,
        'title' : 'aankoop',
        'subject' :'purchase',
        'delete_message' : 'Wil je deze aankoop EN alle verbonden activa verwijderen?',
        'template' : [
            {'name': 'Id', 'data': 'id', 'order_by': Purchase.id},
            {'name': 'Factuur', 'data': 'invoice', 'order_by': Purchase.invoice},
            {'name': 'Bedrag', 'data': 'value', 'order_by': Purchase.value},
            {'name': 'Datum', 'data': 'since', 'order_by': Purchase.since},
            {'name': 'Aantal', 'data': 'nbr_assets', 'order_by': Purchase.nbr_assets},
            {'name': 'Leverancier', 'data': 'supplier.name', 'order_by': Supplier.name},
            {'name': 'Toestel', 'data': 'device.brandtype', 'order_by':Device.brand}],
        'filter' :  ['since', 'value', 'invoice', 'supplier', 'device'],
        'href': [
            {'attribute': '["value"]', 'route': '"purchase.view"', 'id': '["id"]'},
            {'attribute': '["invoice"]', 'route': '"purchase.view"', 'id': '["id"]'},
            {'attribute': '["supplier"]["name"]', 'route': '"supplier.view"', 'id': '["supplier"]["id"]'},
            {'attribute': '["device"]["brandtype"]', 'route': '"device.view"', 'id': '["device"]["id"]'}
                ],
        'floating_menu' : default_menu_config,
    },
    'device': {
        'model': Device,
        'title' : 'toestel',
        'subject' :'device',
        'delete_message' : 'Wil je dit toestel EN alle verbonden aankopen EN activa verwijderen?',
        'template': [
            {'name': 'Merk', 'data': 'brand', 'order_by': Device.brand},
            {'name': 'Type', 'data': 'type', 'order_by': Device.type},
            {'name': 'Categorie', 'data': 'category', 'order_by': DeviceCategory.name},
            {'name': 'CE', 'data': 'ce', 'order_by': Device.ce},
            {'name': 'Vermogen', 'data': 'power', 'order_by': Device.power}],
        'filter': ['category', 'device'],
        'href': [{'attribute': '["brand"]', 'route': '"device.view"', 'id': '["id"]'},
                 ],
        'floating_menu' : default_menu_config,
    },
    'supplier': {
        'model': Supplier,
        'title' : 'leverancier',
        'route' : 'supplier.suppliers',
        'subject' :'supplier',
        'delete_message' : 'Wil je deze leverancier EN alle verbonden aankopen EN activa verwijderen?',
        'template': [
            {'name': 'Naam', 'data': 'name', 'order_by': Supplier.name},
            {'name': 'Beschrijving', 'data' : 'description', 'order_by': Supplier.description}],
        'filter': ['supplier'],
        'href': [{'attribute': '["name"]', 'route': '"supplier.view"', 'id': '["id"]'},
                 ],
        'floating_menu' : default_menu_config,
    },
    'user': {
        'model': User,
        'title' : 'gebruiker',
        'subject' :'management.user',
        'delete_message' : '',
        'template': [
            {'name': 'Gebruikersnaam', 'data': 'username', 'order_by': User.username},
            {'name': 'Voornaam', 'data': 'first_name', 'order_by': User.first_name},
            {'name': 'Naam', 'data': 'last_name', 'order_by': User.last_name},
            {'name': 'Email', 'data': 'email', 'order_by': User.email},
            {'name': 'Niveau', 'data': 'level', 'order_by': User.level, 'orderable': True},
        ],
        'filter': [],
        'href': [
            {'attribute': '["username"]', 'route': '"management.user.view"', 'id': '["id"]'},
        ],
        'floating_menu' : default_menu_config,
        'query_filter' : filter,
    },
    'device_category': {
        'model': DeviceCategory,
        'title' : 'Toestel Categorie',
        'subject' :'management.device_category',
        'delete_message' : '',
        'template': [
            {'name': 'Naam', 'data': 'name', 'order_by': DeviceCategory.name, 'width': '2%'},
            {'name': 'Actief', 'data': 'active', 'order_by': DeviceCategory.active, 'width': '1%'},
            {'name': 'Info', 'data': 'info', 'order_by': DeviceCategory.info, 'width': '50%'},
        ],
        'filter': [],
        'floating_menu' : edit_add_view_menu_config,
        'href': [
            {'attribute': '["name"]', 'route': '"management.device_category.view"', 'id': '["id"]'},
        ],
    }
}

