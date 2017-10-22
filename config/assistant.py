#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

config/assistant.py - Configuration assistant.
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import logging
import os
import sqlite3
import re
import hashlib
import getpass

import database as db

#-----------------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------------
def main():
    """
    Creates database, tables and ask for user parameters.
    Defined parameters :
    - BUZZER_ON
    - BUZZER_POT
    - CAMERA_RES_X
    - CAMERA_RES_Y
    - USER_PASSWORD
    """
    # Intro
    print("-"*80)
    print("Configuring Jean-Pierre, the groceries helper bot :{o")
    print("-"*80)

    # Create / connects to the database
    db.Connect()
    print("SQlite3 database created.")

    # Create table : params
    paramsdb = db.ParamsTable()
    paramsdb.create()
    print("Params table created if not already set.")

    # Create table : groceries
    groceriesdb = db.GroceriesTable()
    groceriesdb.create()
    print("Groceries table created if not already set.")

    # Create table : products
    productsdb = db.ProductsTable()
    productsdb.create()
    print("Products table created if not already set.")

    # Ask for : use buzzer / on which port ?
    paramsdb.delete_item('BUZZER_ON')
    paramsdb.delete_item('BUZZER_PORT')

    buzzer_on = input("Shall we use a buzzer (Y/N) : ")

    # Yes
    if buzzer_on.upper() == "Y":
        buzzer_port = input("On which GPIO port is the buzzer connected : ")
        if re.findall('([0-9]+)', buzzer_port):
            paramsdb.add_item('BUZZER_ON', '1')
            paramsdb.add_item('BUZZER_PORT', buzzer_port)
        else:
            print("Invalid GPIO port number : moving on.")
    # No
    else:
        paramsdb.add_item('BUZZER_ON', '0')
        paramsdb.add_item('BUZZER_PORT', '')

    # Ask for : camera resolution ?
    paramsdb.delete_item('CAMERA_RES_X')
    paramsdb.delete_item('CAMERA_RES_Y')

    for axis in ['X', 'Y']:
        question = "Camera resolution, {} (500 by default) : "
        if axis == 'X':
            question = question.format('WIDTH')
        else:
            question = question.format('HEIGHT')

        resolution = input(question)
        if not re.findall('([0-9]+)', resolution):
            resolution = 500
        paramsdb.add_item('CAMERA_RES_{}'.format(axis), resolution)

    # Ask for : user password
    paramsdb.delete_item('USER_PASSWORD')
    user_password = getpass.getpass("Please define a password for Jean-Pierre : ")
    user_password = bytearray(user_password, encoding='utf-8')
    user_password = hashlib.sha1(user_password).hexdigest()
    paramsdb.add_item('USER_PASSWORD', user_password)

    # Close connection to the database
    db.Connect().disconnect()

    # Bye !
    print("All set ! Enjoy !")

# Execute
if __name__ == "__main__":
    try:
        main()
    except Warning as trace:
        logging.warning(trace, exc_info=True)
    except Exception as trace:
        logging.error(trace, exc_info=True)
