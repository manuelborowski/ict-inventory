import config, os
print config.DB_TOOLS
config.DB_TOOLS = True
from app import models, db
from app import create_app
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

print('start db tools')

# start...
def fillTables():
    NBR_SUPPLIER=91
    NBR_DEVICE=111
    NBR_PURCHASE=743
    NBR_ASSET=5012
    for i in range(0, NBR_SUPPLIER):
        db.session.add(models.Supplier(name="Leverancier{}".format(i), description="Beschrijving Leverancier{} : telefoonnummer, adres, contactpersoon".format(i)))
    db.session.commit()
    sid = models.Supplier.query.first().id
    print("Leveranciers toegevoegd")

    cat = ['PC', 'BEAMER', 'PRINTER', 'OTHER']
    for i in range(0, NBR_DEVICE):
        db.session.add(models.Device(brand='brand{}'.format(i), type='type{}'.format(i), category=cat[i % 4], power=i, ce=True))
    db.session.commit()
    did = models.Device.query.first().id
    print("Toestellen toegevoegd")

    for i in range(0, NBR_PURCHASE):
        db.session.add(models.Purchase(since=models.Purchase.reverse_date('10-10-{}'.format(2000 + i % 17)), value=i*10, \
                                       supplier_id=(sid +(i % NBR_SUPPLIER)), device_id=(did + (i % NBR_DEVICE))))
    db.session.commit()
    pid = models.Purchase.query.first().id
    print("Aankopen toegevoegd")

    stat = ['IN SERVICE', 'BROKEN', 'IN REPAIR', 'TO BE REPLACED', 'OTHER']
    for i in range(0, NBR_ASSET):
        db.session.add(models.Asset(name='Toestel{}'.format(i), qr_code=i, status=stat[i % 5], location='E2.0{}'.format(i % 10), purchase_id=(pid + (i % NBR_PURCHASE))))
    db.session.commit()
    print("Items     toegevoegd")

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
