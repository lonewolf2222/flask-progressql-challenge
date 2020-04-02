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

@app.route("/store_index")
def store_index():
    stores = Store.select()
    return render_template('store_index.html', stores= stores)

@app.route("/store_new")
def store_new():
    return render_template('store_new.html')

@app.route("/store_create", methods=["POST"])
def store_create():
    store_name = request.form.get('store_name')
    try:
        Store.create(name=store_name)
        flash("Store created")
        return redirect(url_for('store_new'))
    except:
        flash("Store name exists!")
        return redirect(url_for('store_new'))

@app.route("/warehouse_new")
def warehouse_new():
    stores = Store.select()
    return render_template('warehouse_new.html', stores=stores)

@app.route("/warehouse_create",methods=["POST"])
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