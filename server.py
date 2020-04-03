import peeweedbevolve
from flask import Flask, render_template, request, redirect, flash, url_for
from models import *

app = Flask(__name__)
app.secret_key = b'\xecS\xca\xb0\xc21\n\x0e'

@app.before_request
def before_request():
   db.connect()

@app.after_request 
def after_request(response):
   db.close()
   return response

@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/store/index")
def store_index():
    stores = Store.select()
    return render_template('store_index.html', stores= stores)

@app.route("/store/<id>")
def store_show(id):
    id = int(id)
    stores = Store.select()
    if len(stores) >= id:
        store = Store.get_by_id(id)
        warehouses = store.warehouses
        num_warehouses = len(warehouses)
        store_name = store.name
        return render_template('store_show.html', num_warehouses=num_warehouses, store_name=store_name)
    else:
        return redirect(url_for('index'))

@app.route("/store/new")
def store_new():
    return render_template('store_new.html')

@app.route("/store/create", methods=["POST"])
def store_create():
    store_name = request.form.get('store_name')
    try:
        Store.create(name=store_name)
        flash("Store created")
        return redirect(url_for('store_new'))
    except:
        flash("Store name exists!")
        return redirect(url_for('store_new'))

@app.route("/store/edit/<id>")
def store_edit(id):
    id =int(id)
    store = Store.get_by_id(id)
    return render_template('store_edit.html', store=store)

@app.route("/store/<store_id>", methods=["POST"])
def store_update(store_id):
    new_name = request.form.get('new_name')
    try:
        query = Store.update(name =new_name).where(Store.id == store_id)
        query.execute()
        flash("Store name updated")
        return redirect(url_for('store_edit', id=store_id))
    except:
        flash("An error has occurred")
        return redirect(url_for('store_edit', id=store_id))

@app.route("/stores")
def stores():
    stores = Store.select()
    return render_template('store_index.html', stores=stores)

@app.route("/stores/delete", methods=["POST"])
def store_destroy():
    store_name = request.form.get('store_name')
    store = Store.get(Store.name == store_name)
    store.delete_instance()
    flash("Store deleted")
    return redirect(url_for('stores'))

@app.route("/warehouse/new")
def warehouse_new():
    stores = Store.select()
    return render_template('warehouse_new.html', stores=stores)

@app.route("/warehouse/create",methods=["POST"])
def warehouse_create():
    location = request.form.get('location')
    store = request.form.get('store')
    try:
        Warehouse.create(store=store, location=location)
        flash("Warehouse created")
        return redirect(url_for('warehouse_new'))
    except:
        flash("An error has occurred")
        return redirect(url_for('warehouse_new'))

if __name__ == '__main__':
   app.run()