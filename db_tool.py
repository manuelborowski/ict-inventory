import config, os
from app import models, db, create_app
from app import create_app
import sys, getopt

app=None

def print_help():
    print 'db_tool.py -hcpl'
    print '-c : clear database'
    print '-p : populuta database, 500 assets'
    print '-pl : populate database, 30000 assets'
    sys.exit(2)

# start...
def fillTables(large=False):
    if large:
        NBR_SUPPLIER=331
        NBR_DEVICE=991
        NBR_PURCHASE=5023
        NBR_ASSET=33987
    else:
        NBR_SUPPLIER=89
        NBR_DEVICE=91
        NBR_PURCHASE=217
        NBR_ASSET=523
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




#fillTables()


def main(argv):
    config.DB_TOOLS = True
    config_name = os.getenv('FLASK_CONFIG')
    app = create_app(config_name)

    _populate = False
    _populate_large = False
    try:
        opts, args = getopt.getopt(argv,"hcpl")
    except getopt.GetoptError:
        print_help()
    for opt, arg in opts:
        if opt == '-h':
            print_help()
        if opt in ("-c"):
            print 'clearing database'
            dropTables()
            create_admin()
        if opt in ("-p"):
            _populate = True
        if opt in ("-l") and _populate:
            _populate_large = True

    if _populate:
        if _populate_large:
            print 'populating database with many assets'
            fillTables(True)
        else:
            print 'populating database'
            fillTables(False)


if __name__ == "__main__":
   main(sys.argv[1:])