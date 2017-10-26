#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

jeanpierre.py - Main script
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import logging
import argparse
import os

import controllers
from controllers.web import webapp # Gunicorn hook for Flask

#-----------------------------------------------------------------------------
# Main : routing
#-----------------------------------------------------------------------------
def main():
    """
    Routing from the console line arguments to the appropriate controller.
    Options :
    --do config/scanner/web
    """
    # Get arguments
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-d", "--do",
                           help="Jean-Pierre's process to launch: config/scanner/web")
    arguments = arguments.parse_args()

    # If no arguments
    if not arguments or not hasattr(arguments, 'do') or not arguments.do:
        message = "Jean-Pierre understands:\n"
        message += "--do config : launch the configuration assistant"
        message += "--do scanner : launch the scanner process"
        message += "--do web : launch the web server"
        print(message)
        return

    # If invalid arguments
    if arguments.do not in ['config', 'scanner', 'web']:
        message = 'Invalid option --do "{}"'.format(arguments.do)
        print(message)
        return

    # Check that the program has been configured
    if arguments.do != 'config' and not os.path.isfile('database.db'):
        message = "Jean-Pierre is not configured. Please launch jeanpierre.py --do config"
        print(message)
        return

    # Call the appropriate controller
    if arguments.do == 'config':
        controllers.Config.execute()
    elif arguments.do == 'scanner':
        controllers.Scanner.execute()
    elif arguments.do == 'web':
        webapp.run(debug=True, host='0.0.0.0')
        print("Flask launched in DEBUG mode.")
        print("For production, please use : gunicorn --bind 0.0.0.0 jeanpierre:webapp")

# Execution
if __name__ == "__main__":
    try:
        main()
    except Warning as trace:
        logging.warning(trace, exc_info=True)
    except Exception as trace:
        logging.error(trace, exc_info=True)
