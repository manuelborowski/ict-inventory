import config, os

print config.DB_TOOLS
config.DB_TOOLS = True
from app import models, db


_suppliers = [
    models.Supplier(name="Leverancier 1", description="Beschrijving Leverancier 1"),
    models.Supplier(name="Leverancier 2", description="Beschrijving Leverancier 2")
]

_devices = [
    models.Device(brand='Hitachi', type='XL34D', category='BEAMER', power=345.5, ce=True),
    models.Device(brand='Intel', type='NUC32333', category='PC', power=23, ce=True)
]

_purchases = [
    models.Purchase(since=models.Purchase.reverse_date('10-10-2012'), value=100.25),
    models.Purchase(since=models.Purchase.reverse_date('10-10-2013'), value=900.00),
    models.Purchase(since=models.Purchase.reverse_date('10-10-2013'), value=210.23),
    models.Purchase(since=models.Purchase.reverse_date('10-10-2014'), value=6734.34)
]

_assets = [
    models.Asset(name='Beamer 1', qr_code=1, status='IN SERVICE', location='E2.01'),
    models.Asset(name='Beamer 2', qr_code=2, status='IN REPAIR', location='E2.02'),
    models.Asset(name='PC 1', qr_code=3, status='BROKEN', location='E2.03'),
    models.Asset(name='PC 2', qr_code=4, status='IN SERVICE', location='E2.03'),
    models.Asset(name='PC 3', qr_code=5, status='IN SERVICE', location='E2.04')
]


print('start db tools')


# start...
def newItem(i, itype, iname):
    try:
        db.session.add(i)
        db.session.commit()
        print('added {} : {}'.format(itype, iname))
    except Exception as e:
        db.session.rollback()
        print e
        print('{} : {} already exists'.format(itype, iname))


def linkAssetToPurchase(qr_code, date, value):
    try:
        p = models.Purchase.query.filter(models.Purchase.since==models.Purchase.reverse_date(date), models.Purchase.value==value).first()
        a = models.Asset.query.filter(models.Asset.qr_code==qr_code).first()
        p.assets.append(a)
        db.session.commit()
        print('linked asset {} to purchase {}/{}'.format(qr_code, date, value))
    except Exception as e:
        print(str(e))
        db.session.rollback()
        print('could not link asset {} to purchase {}/{}'.format(qr_code, date, value))

def linkPurchaseToDevice(date, value, category):
    try:
        p = models.Purchase.query.filter(models.Purchase.since==models.Purchase.reverse_date(date), models.Purchase.value==value).first()
        d = models.Device.query.filter(models.Device.category==category).first()
        d.purchases.append(p)
        db.session.commit()
        print('linked purchase {}/{} to device {}'.format(date, value, category))
    except Exception as e:
        print(str(e))
        db.session.rollback()
        print('could not link purchase {}/{} to device {}'.format(date, value, category))

def linkPurchaseToSupplier(date, value, name):
    try:
        p = models.Purchase.query.filter(models.Purchase.since==models.Purchase.reverse_date(date), models.Purchase.value==value).first()
        s = models.Supplier.query.filter(models.Supplier.name==name).first()
        s.purchases.append(p)
        db.session.commit()
        print('linked purchase {}/{} to supplier {}'.format(date, value, name))
    except Exception as e:
        print(str(e))
        db.session.rollback()
        print('could not link purchase {}/{} to supplier {}'.format(date, value, name))

def fillTables():
    for s in _suppliers:
        newItem(s, 'Supplier', s.name)

    for d in _devices:
        newItem(d, 'Device', d.brand)

    for p in _purchases:
        newItem(p, 'Purchase', p.since)

    for a in _assets:
        newItem(a, 'Asset', a.name)

    linkAssetToPurchase(1, '10-10-2012', 100.25)
    linkAssetToPurchase(2, '10-10-2013', 900)
    linkAssetToPurchase(3, '10-10-2014', 6734.34)
    linkAssetToPurchase(4, '10-10-2014', 6734.34)
    linkAssetToPurchase(5, '10-10-2013', 210.23)

    linkPurchaseToDevice('10-10-2012', 100.25, 'BEAMER')
    linkPurchaseToDevice('10-10-2013', 900, 'BEAMER')
    linkPurchaseToDevice('10-10-2014', 6734.34, 'PC')
    linkPurchaseToDevice('10-10-2014', 6734.34, 'PC')
    linkPurchaseToDevice('10-10-2013', 210.23, 'PC')

    linkPurchaseToSupplier('10-10-2012', 100.25, 'Leverancier 1')
    linkPurchaseToSupplier('10-10-2013', 900, 'Leverancier 2')
    linkPurchaseToSupplier('10-10-2014', 6734.34, 'Leverancier 1')
    linkPurchaseToSupplier('10-10-2014', 6734.34, 'Leverancier 1')
    linkPurchaseToSupplier('10-10-2013', 210.23, 'Leverancier 2')



def dropTables():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()

def create_admin():
    from app.models import User
    admin = User(username='admin', password='admin', is_admin=True)
    db.session.add(admin)
    db.session.commit()


from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

dropTables()
create_admin()
fillTables()

print('stop db tools')
