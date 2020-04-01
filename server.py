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

@app.route("/create", methods=["POST"])
def create():
    store_name = request.form.get('store_name')
    # s = Store.create(name=store_name)
    try:
        Store.create(name=store_name)
        #flash("Store created")
        return redirect(url_for('store'))
    except:
        #flash("Store name exists!")
        return redirect(url_for('store'))

if __name__ == '__main__':
   app.run()