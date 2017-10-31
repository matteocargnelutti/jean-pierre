#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot that helps people make their grocery list.
Matteo Cargnelutti - github.com/matteocargnelutti

controllers/web.py - Web server : uses Flask
Defines views and a handy controller class.
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os
import random
import string
import hashlib
import json

from flask import Flask, render_template, session, request, redirect, url_for

from utils import Database
import utils
import models

#-----------------------------------------------------------------------------
# Flask WSGI init
#-----------------------------------------------------------------------------
if __name__ != '__main__':

    #
    # Generate / retrieve secret key
    #
    webapp_secret_key = ''
    # Is there a secret key ?
    if os.path.isfile('flask_secret_key'):
        with open('flask_secret_key', 'r') as file:
            webapp_secret_key = file.read()
    # If there's none : generate a new one
    else:
        with open('flask_secret_key', 'w') as file:
            newkey = "".join([random.choice(string.printable) for _ in range(24)])
            file.write(newkey)
            webapp_secret_key = newkey
            del newkey

    #
    # Define Folders
    #
    path = os.path.abspath(os.path.dirname(__file__))
    path = path.replace('controllers', '')
    webapp_folders = {
        'static': path + '/assets/static',
        'templates': path + '/assets/templates'
    }
    del path

    #
    # Flask init
    #
    webapp = Flask(__name__,
                   static_url_path='/static',
                   static_folder=webapp_folders['static'],
                   template_folder=webapp_folders['templates'])
    webapp.config['SECRET_KEY'] = webapp_secret_key

#-----------------------------------------------------------------------------
# Views
#-----------------------------------------------------------------------------
@webapp.route('/', methods=['GET', 'POST'])
def login():
    """
    Landing page.
    Launches and handles login form if needed.
    """
    # Database access + loads basic info
    Database.on()
    params = models.Params()
    lang = utils.Lang(params.lang)
    Database.off()

    # If the user is already logged : go to "grocery_list"
    if 'is_logged' in session and session['is_logged']:
        return redirect(url_for('groceries'))

    # If no post data : login form
    if not request.form:
        return render_template('login.html', lang=lang)

    # Handle post data
    if 'password' in request.form:
        password = request.form['password']
        password = bytearray(password, encoding='utf-8')
        password = hashlib.sha1(password).hexdigest()

        # Right password
        if password == params.user_password:
            session['is_logged'] = True
            return redirect(url_for('groceries'))
        # Wrong password
        else:
            return render_template('login.html', lang=lang, error=True)

@webapp.route('/logout')
def logout():
    """
    Logs the user out
    """
    # Loggin check
    if 'is_logged' in session:
        del session['is_logged']

    # Redirection
    return redirect(url_for('login'))

@webapp.route('/groceries')
def groceries():
    """
    Shows GROCERIES template if the user is logged.
    """
    # Loggin check
    if not session['is_logged']:
        return redirect(url_for('login'))

    # Database access + loads basic info
    Database.on()
    lang = utils.Lang(models.Params().lang)
    items = models.Products().get_list()
    Database.off()

    # Return template
    return render_template('groceries.html',
                           lang=lang,
                           products_list=items)

@webapp.route('/groceries_list')
def groceries_list():
    """
    AJAX method : Gets all items from the grocery list.
    Outputs JSON.
    Returns the latest version of the grocery list.
    JSON format :
    - {"status": ..., "items" ...}
    Possible return status :
    - OK
    """
    # Auth check
    if not session['is_logged']:
        return render_template('json.html', json="{}"), 401

    # Output
    data = {"status": "OK", "items": []}

    # Get info
    Database.on()
    data['items'] = models.Groceries().get_list()
    Database.off()

    # Render
    return render_template('json.html', json=json.dumps(data))

@webapp.route('/groceries_edit/<string:barcode>/<int:quantity>')
def groceries_edit(barcode, quantity):
    """
    AJAX method : Add/Edit/Delete items from the grocery list.
    Outputs JSON.
    :param barcode: A known product barcode
    :param quantity: The quantity defines the operation (quantity 0 = delete)
    JSON format :
    - {"status": ..., "barcode" ..., "quantity": ...}
    Possible return status :
    - PRODUCT NOT FOUND
    - ADDED / ADD ERROR
    - EDITED / EDIT ERROR
    - DELETED / DELETE ERROR
    """
    # Auth check
    if not session['is_logged']:
        return render_template('json.html', json="{}"), 401

    # Output
    data = {"status": "", "barcode": barcode, "quantity": quantity}

    # Database access
    Database.on()
    products_db = models.Products()
    groceries_db = models.Groceries()

    # Try to get the product associated with the barcode
    product = products_db.get_item(barcode)

    if not product:
        data['status'] = 'PRODUCT NOT FOUND'
        return render_template('json.html',
                               json=json.dumps(data)), 404

    # Try to get the entry in the grocery list
    with groceries_db.get_item(barcode) as exists:

        # If it doesn't exist : add it
        if not exists:
            try:
                groceries_db.add_item(barcode, quantity)
                data['status'] = 'ADDED'
            except Exception as trace:
                data['status'] = 'ADD ERROR'
        # If it exists :
        else:
            # If quantity = 0 : Delete
            if quantity <= 0:
                try:
                    groceries_db.delete_item(barcode)
                    data['status'] = 'DELETED'
                except Exception as trace:
                    data['status'] = 'DELETE ERROR'
            # If quantity > 0 : Edit quantity
            else:
                try:
                    groceries_db.edit_item(barcode, quantity)
                    data['status'] = 'EDITED'
                except Exception as trace:
                    data['status'] = 'EDIT ERROR'

    # Database : off and outputs data
    Database.off()
    return render_template('json.html', json=json.dumps(data))

@webapp.route('/products')
def products():
    """
    Shows PRODUCTS template if the user is logged.
    """
    # Auth check
    if not session['is_logged']:
        return redirect(url_for('login'))

    # Database access + loads basic info
    Database.on()
    lang = utils.Lang(models.Params().lang)
    Database.off()

    # Return template
    return render_template('products.html', lang=lang)

@webapp.route('/products_list')
def products_list():
    """
    AJAX method : Gets all items from the products table.
    Outputs JSON.
    Returns the latest version of the grocery list.
    JSON format :
    - {"status": ..., "items" ...}
    Possible return status :
    - OK
    """
    # Auth check
    if not session['is_logged']:
        return render_template('json.html', json="{}"), 401

    # Output
    data = {"status": "OK", "items": []}

    # Get info
    Database.on()
    data['items'] = models.Products().get_list()
    Database.off()

    # Render
    return render_template('json.html', json=json.dumps(data))

@webapp.route('/products_edit/<string:barcode>/<string:name>')
def products_edit(barcode, name):
    """
    AJAX method : Add/Edit/Delete items from the grocery list.
    Outputs JSON.
    :param barcode: An unknown product barcode
    :param name: The new product's name
    JSON format :
    - {"status": ..., "barcode" ..., "name": ...}
    Possible return status :
    - ADDED / ADD ERROR
    - EDITED / EDIT ERROR
    """
    # Auth check
    if not session['is_logged']:
        return render_template('json.html', json="{}"), 401

    # Output
    data = {"status": "", "barcode": barcode, "name": name}

    # Database access
    Database.on()
    products_db = models.Products()

    # Try to get the entry in the grocery list
    with products_db.get_item(barcode) as exists:

        # If it doesn't exist : add it
        if not exists:
            try:
                products_db.add_item(barcode, name, '')
                data['status'] = 'ADDED'
            except Exception as trace:
                data['status'] = 'ADD ERROR'
        # If it exists : edit it
        else:
            try:
                products_db.edit_item(barcode, name, '')
                data['status'] = 'EDITED'
            except Exception as trace:
                data['status'] = 'EDIT ERROR'

    # Database : off and outputs data
    Database.off()
    return render_template('json.html', json=json.dumps(data))

@webapp.route('/products_delete/<string:barcode>')
def products_delete(barcode):
    """
    AJAX method : Deletes an item from the products table.
    Outputs JSON.
    Returns the latest version of the grocery list.
    JSON format :
    - {"status": ...}
    Possible return status :
    - OK
    - DELETE ERROR
    """
    # Auth check
    if not session['is_logged']:
        return render_template('json.html', json="{}"), 401

    # Output
    data = {"status": "OK"}

    # Try to delete
    Database.on()
    try:
        models.Products().delete_item(barcode)
        data['status'] = 'OK'
    except Exception as trace:
        data['status'] = 'DELETE ERROR'
    Database.off()

    # Render
    return render_template('json.html', json=json.dumps(data))
