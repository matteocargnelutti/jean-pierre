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
        file = open('flask_secret_key', 'r')
        secret_key = file.read()
        file.close()
        webapp_secret_key = secret_key
    # If there's none : generate a new one
    else:
        secret_key = "".join([random.choice(string.printable) for _ in range(24)])
        file = open('flask_secret_key', 'w')
        file.write(secret_key)
        file.close()
        webapp_secret_key = secret_key
    del file

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
def landing():
    """
    Landing page.
    Launches login form if needed.
    """
    # Database access + loads basic info
    Database.on()
    params = models.Params()
    lang = utils.Lang(params.lang)
    Database.off()

    # If the user is already logged : go to "grocery_list"
    if 'is_logged' in session and session['is_logged']:
        return redirect(url_for('grocery_list'))

    # If no post data : login form
    if not request.form:
        return render_template('login.html', lang=lang)

    # Handle post data
    if 'password' in request.form:
        password = request.form['password']
        password = bytearray(password, encoding='utf-8')
        password = hashlib.sha1(password).hexdigest()

        if password == params.user_password:
            session['is_logged'] = True
            return render_template('login.html', lang=lang, error=True)
        else:
            return redirect(url_for('grocery_list'))

@webapp.route('/my-list')
def grocery_list():
    """
    Grocery list page.
    Only accessible if logged
    """
    return render_template('logged.html')
