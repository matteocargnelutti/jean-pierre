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
    Grocery list page.
    Only accessible if logged.
    """
    # Loggin check
    if not session['is_logged']:
        return redirect(url_for('login'))

    # Database access + loads basic info
    Database.on()
    params = models.Params()
    lang = utils.Lang(params.lang)
    Database.off()

    # Return template
    return render_template('groceries.html', lang=lang)

@webapp.route('/groceries_list')
def groceries_list():
    """
    AJAX method : Add/Edit/Delete items from the grocery list.
    Outputs JSON.
    Returns the latest version of the grocery list.
    JSON format :
    - {"status": ..., "items" ...}
    Possible return status :
    - OK
    """
    # Loggin check
    if not session['is_logged']:
        return redirect(url_for('login'))

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
    - ADDED
    - EDITED
    - DELETED
    """
    # Loggin check
    if not session['is_logged']:
        return redirect(url_for('login'))

    # Output
    data = {"status": "", "barcode": barcode, "quantity": quantity}

    # Database connexion + load basic infos
    Database.on()
    products = models.Products()
    groceries = models.Groceries()

    # Try to get the product associated with the barcode
    product = products.get_item(barcode)

    if not product:
        data['status'] = 'PRODUCT NOT FOUND'
        return render_template('json.html',
                               json=json.dumps(data)), 404

    # Try to get the entry in the grocery list
    with groceries.get_item(barcode) as exists:

        # If it doesn't exist : add it
        if not exists:
            groceries.add_item(barcode, quantity)
            data['status'] = 'ADDED'
        # If it exists :
        else:
            # If quantity = 0 : Delete
            if quantity <= 0:
                groceries.delete_item(barcode)
                data['status'] = 'DELETED'
            # If quantity > 0 : Edit quantity
            else:
                groceries.edit_item(barcode, quantity)
                data['status'] = 'EDITED'

    # Database : off and outputs data
    Database.off()
    return render_template('json.html', json=json.dumps(data))
