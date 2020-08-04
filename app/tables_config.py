from .models import Asset, Purchase, Device, Supplier, User, DeviceCategory, AssetLocation, Invoice
from .management.user.extra_filtering import filter
from .floating_menu import default_menu, user_menu, no_delete_menu

tables_configuration = {
    'asset' : {
        'model' : Asset,
        'title' : 'activa',
        'subject' :'asset',
        'delete_message' : '',
        'template' : [
            {'name': 'Naam', 'data':'name', 'order_by': Asset.name},
            {'name': '#', 'data':'quantity', 'order_by': Asset.quantity},
            {'name': 'Factuur', 'data':'purchase.invoice.number', 'order_by': Invoice.number},
            {'name': 'Lijn ID', 'data':'purchase.id', 'order_by': Purchase.id},
            {'name': 'Categorie', 'data':'purchase.device.category.name', 'order_by': DeviceCategory.name},
            {'name': 'Locatie', 'data':'location.name', 'order_by': AssetLocation.name},
            {'name': 'Datum', 'data':'purchase.invoice.since', 'order_by': Invoice.since},
            {'name': 'Bedrag', 'data':'purchase.asset_value', 'order_by': Purchase.asset_value},
            {'name': 'QR', 'data':'qr_code', 'order_by': Asset.qr_code},
            {'name': 'Status', 'data':'status', 'order_by': Asset.status},
            {'name': 'Leverancier', 'data':'purchase.invoice.supplier.name', 'order_by': Supplier.name},
            {'name': 'Toestel', 'data':'purchase.device.brandtype', 'order_by': Device.brand},
            {'name': 'SerieNr', 'data': 'serial', 'order_by': Asset.serial}],
        'filter' :  ['since', 'invoice', 'location', 'category', 'status', 'supplier', 'device', 'purchase_id'],
        'href': [
            {'attribute': '["name"]', 'route': '"asset.view"', 'id': '["id"]'},
            {'attribute': '["purchase"]["invoice"]["number"]', 'route': '"invoice.view"', 'id': '["purchase"]["invoice"]["id"]'},
            {'attribute': '["purchase"]["id"]', 'route': '"purchase.view"', 'id': '["purchase"]["id"]'},
            {'attribute': '["purchase"]["invoice"]["supplier"]["name"]', 'route': '"supplier.view"', 'id': '["purchase"]["invoice"]["supplier"]["id"]'},
            {'attribute': '["purchase"]["device"]["brandtype"]', 'route': '"device.view"', 'id': '["purchase"]["device"]["id"]'}
        ],
        'floating_menu' : default_menu,
        'export' : 'asset.exportcsv',
    },
    'purchase' : {
        'model' : Purchase,
        'title' : 'aankoop',
        'subject' :'purchase',
        'delete_message' : 'Wil je deze aankoop EN alle verbonden activa verwijderen?',
        'template' : [
            {'name': 'Lijn ID', 'data': 'id', 'order_by': Purchase.id},
            {'name': 'Factuur', 'data': 'invoice.number', 'order_by': Invoice.number},
            {'name': 'Bedrag', 'data': 'value', 'order_by': Purchase.value},
            {'name': 'Datum', 'data': 'invoice.since', 'order_by': Invoice.since},
            {'name': 'Aantal', 'data': 'nbr_assets', 'order_by': Purchase.nbr_assets},
            {'name': 'Leverancier', 'data': 'invoice.supplier.name', 'order_by': Supplier.name},
            {'name': 'Toestel', 'data': 'device.brandtype', 'order_by':Device.brand}],
        'filter' :  ['since', 'invoice', 'supplier', 'device'],
        'href': [
            {'attribute': '["value"]', 'route': '"purchase.view"', 'id': '["id"]'},
            {'attribute': '["invoice"]["number"]', 'route': '"invoice.view"', 'id': '["invoice"]["id"]'},
            {'attribute': '["invoice"]["supplier"]["name"]', 'route': '"supplier.view"', 'id': '["invoice"]["supplier"]["id"]'},
            {'attribute': '["device"]["brandtype"]', 'route': '"device.view"', 'id': '["device"]["id"]'}
            ],
        'floating_menu' : default_menu,
    },
    'invoice' : {
        'model' : Invoice,
        'title' : 'Factuur',
        'subject' :'invoice',
        'delete_message' : 'Wil je deze Factuur EN alle verbonden activa verwijderen?',
        'template' : [
            {'name': 'Factuur', 'data': 'number', 'order_by': Invoice.number},
            {'name': 'Datum', 'data': 'since', 'order_by': Invoice.since},
            {'name': 'Leverancier', 'data': 'supplier.name', 'order_by': Supplier.name},
            {'name': 'Info', 'data': 'info', 'order_by': Invoice.info}],
        'filter' :  ['since', 'invoice', 'supplier'],
        'href': [
            {'attribute': '["number"]', 'route': '"invoice.view"', 'id': '["id"]'},
            {'attribute': '["supplier"]["name"]', 'route': '"supplier.view"', 'id': '["supplier"]["id"]'},
            ],
        'floating_menu' : default_menu,
    },
    'device': {
        'model': Device,
        'title' : 'toestel',
        'subject' :'device',
        'delete_message' : 'Wil je dit toestel EN alle verbonden aankopen EN activa verwijderen?',
        'template': [
            {'name': 'Merk', 'data': 'brand', 'order_by': Device.brand},
            {'name': 'Type', 'data': 'type', 'order_by': Device.type},
            {'name': 'Categorie', 'data': 'category.name', 'order_by': DeviceCategory.name},
            {'name': 'CE', 'data': 'ce', 'order_by': Device.ce},
            {'name': 'Vermogen', 'data': 'power', 'order_by': Device.power}],
        'filter': ['category', 'device'],
        'href': [{'attribute': '["brand"]', 'route': '"device.view"', 'id': '["id"]'},
                 ],
        'floating_menu' : default_menu,
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
        'floating_menu' : default_menu,
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
        'floating_menu' : user_menu,
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
        'floating_menu' : no_delete_menu,
        'href': [
            {'attribute': '["name"]', 'route': '"management.device_category.view"', 'id': '["id"]'},
        ],
    },
    'asset_location': {
        'model': AssetLocation,
        'title' : 'Locatie',
        'subject' :'management.asset_location',
        'delete_message' : '',
        'template': [
            {'name': 'Naam', 'data': 'name', 'order_by': AssetLocation.name, 'width': '2%'},
            {'name': 'Actief', 'data': 'active', 'order_by': AssetLocation.active, 'width': '1%'},
            {'name': 'Info', 'data': 'info', 'order_by': AssetLocation.info, 'width': '50%'},
        ],
        'filter': [],
        'floating_menu' : no_delete_menu,
        'href': [
            {'attribute': '["name"]', 'route': '"management.asset_location.view"', 'id': '["id"]'},
        ],
    },
}

