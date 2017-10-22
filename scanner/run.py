#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

scanner/run.py - Scanner embed app.
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import logging
import os
import sqlite3

#import picamera

#-----------------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------------
def main():
    """
    Constantly tries to catch barcodes from the camera :
    if it does, search for info and add it to the user's groceries list.
    """
    # Intro
    print("-"*80)
    print("Jean-Pierre Scanner : Running :{o")
    print("-"*80)

    # Database connection
    database_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_path = database_path + "/database.db"

    if not os.path.isfile(database_path):
        raise Exception("No database found. Please use install.sh to configure this app.")

    link = sqlite3.connect(database_path)
    print("Connected to SQlite database.")

# Execute
if __name__ == "__main__":
    try:
        main()
    except Warning as trace:
        logging.warning(trace, exc_info=True)
    except Exception as trace:
        logging.error(trace, exc_info=True)
