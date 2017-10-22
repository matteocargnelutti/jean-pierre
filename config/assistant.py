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
    Creates database, tables and ask for user parameters
    """
    # Intro
    print("-"*80)
    print("Configuring Jean-Pierre, the groceries helper bot :{o")
    print("-"*80)

    # Create / connects to the database
    database_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_path = database_path + "/database.db"
    link = sqlite3.connect(database_path)
    print("SQlite3 database created.")

    # Create table : params
    paramsdb = db.Params(link)
    paramsdb.create_table()
    print("Params table created if not already set.")

    # Create table : groceries
    groceriesdb = db.Groceries(link)
    groceriesdb.create_table()
    print("Groceries table created if not already set.")

    # Create table : products
    productsdb = db.Products(link)
    productsdb.create_table()
    print("Products table created if not already set.")

    # Ask for : use buzzer ?
    paramsdb.delete_item('buzzer_on')
    paramsdb.delete_item('buzzer_port')

    buzzer_on = input("Shall we use a buzzer (Y/N) : ")
    if buzzer_on.upper() == "Y":
        buzzer_port = input("On which GPIO port is the buzzer connected : ")
        if re.findall('([0-9]+)', buzzer_port):
            paramsdb.add_item('buzzer_on', '1')
            paramsdb.add_item('buzzer_port', buzzer_port)
        else:
            print("Invalid GPIO port number : moving on.")

    # Ask for : user password
    paramsdb.delete_item('user_password')
    user_password = getpass.getpass("Please define a password for Jean-Pierre : ")
    user_password = bytearray(user_password, encoding='utf-8')
    user_password = hashlib.sha1(user_password).hexdigest()
    paramsdb.add_item('user_password', user_password)

    # Close connection to the database
    link.close()

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
