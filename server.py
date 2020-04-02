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

@app.route("/store")
def store():
    return render_template('store.html')

@app.route("/create_store", methods=["POST"])
def create_store():
    store_name = request.form.get('store_name')
    try:
        Store.create(name=store_name)
        flash("Store created")
        return redirect(url_for('store'))
    except:
        flash("Store name exists!")
        return redirect(url_for('store'))

@app.route("/get_store")
def get_store():
    stores = Store.select()
    return render_template('warehouse.html', stores=stores)

@app.route("/create_warehouse",methods=["POST"])
def create_warehouse():
    location = request.form.get('location')
    store = request.form.get('store')
    try:
        Warehouse.create(store=store, location=location)
        flash("Warehouse created")
        return redirect(url_for('get_store'))
    except:
        flash("An error has occurred")
        return redirect(url_for('get_store'))

if __name__ == '__main__':
   app.run()