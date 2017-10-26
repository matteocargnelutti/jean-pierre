#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

controllers/config.py - Configuration assistant class
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import random
import string
import re
import hashlib
import getpass

from utils import Database
import models

#-----------------------------------------------------------------------------
# Config controller class
#-----------------------------------------------------------------------------
class Config:
    """
    This controller class handles:
    - Execution of the configuration prompt
    - Database init
    - User parameters storage
    Usage :
    - controllers.Config.execute()
    """
    @classmethod
    def execute(cls):
        """
        Creates database, tables and ask for user parameters.
        Defined parameters :
        - buzzer_on
        - buzzer_port
        - camera_res_x
        - camera_res_y
        - user_password
        """
        # Intro
        print("-"*80)
        print("Configuring Jean-Pierre, the groceries helper bot :{o")
        print("-"*80)

        # Create / connects to the database
        Database.on()
        print("SQlite3 database created.")

        # Create table : params
        params = models.Params(autoload=False)
        params.create_table()
        print("Params table created if not already set.")

        # Create table : groceries
        groceries = models.Groceries()
        groceries.create_table()
        print("Groceries table created if not already set.")

        # Create table : products
        products = models.Products()
        products.create_table()
        print("Products table created if not already set.")

        # Ask for : use buzzer / on which port ?
        params.delete_item('buzzer_on')
        params.delete_item('buzzer_port')
        buzzer_on = input("Shall we use a buzzer (Y/N) : ")

        # Yes
        if buzzer_on.upper() == "Y":
            buzzer_port = input("On which GPIO port is the buzzer connected : ")
            if re.findall('([0-9]+)', buzzer_port):
                params.add_item('buzzer_on', '1')
                params.add_item('buzzer_port', buzzer_port)
            else:
                print("Invalid GPIO port number : moving on.")
                params.add_item('buzzer_on', '0')
                params.add_item('buzzer_port', '0')
        # No
        else:
            params.add_item('buzzer_on', '0')
            params.add_item('buzzer_port', '0')

        # Ask for : camera resolution
        params.delete_item('camera_res_x')
        params.delete_item('camera_res_y')

        for axis in ['x', 'y']:
            question = "Camera resolution, {} (500 by default) : "

            if axis == 'x':
                question = question.format('WIDTH')
            else:
                question = question.format('HEIGHT')

            resolution = input(question)
            if not re.findall('([0-9]+)', resolution):
                resolution = 500

            params.add_item('camera_res_{}'.format(axis), resolution)

        # Ask for : user password
        params.delete_item('user_password')
        user_password = getpass.getpass("Please define a password for Jean-Pierre : ")
        user_password = bytearray(user_password, encoding='utf-8')
        user_password = hashlib.sha1(user_password).hexdigest()
        params.add_item('user_password', user_password)

        # Define a Flask secret key
        params.delete_item('flask_secret_key')
        flask_secret_key = "".join([random.choice(string.printable) for _ in range(24)])
        params.add_item('flask_secret_key', flask_secret_key)

        # Close connection to the database
        Database.off()

        # Bye !
        print("All set ! Enjoy !")
