#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

scanner/utils/findproduct.py
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import re
from threading import Thread, RLock

import requests

import database as db

#-----------------------------------------------------------------------------
# FindProduct class
#-----------------------------------------------------------------------------
class FindProduct(Thread):
    """
    This class handles :
    - Fetch product's from a barcode from the OpenFoodFacts OR local cache
    - Add it to the groceries list OR increase the quantity
    Usage :
    - thread = FindProduct(barcode)
    - thread.start()
    Note : 
    - This class creates its own thread
    """
    LOCK = RLock()
    """ Thread lock """

    def __init__(self, barcode):
        """
        Inits the thread
        :param barcode: Barcode to search
        :type barcode: str
        :rtype: FindProduct
        """
        Thread.__init__(self)
        self.barcode = barcode
        self.name = ''


    def run(self):
        """
        Fetch, gathers, insert product infos.
        Threaded
        :rtype: bool
        """
        with FindProduct.LOCK:
            # Database connection
            db.Connect.on()

            # Marks
            found = False
            cache = False
            products = db.ProductsTable()
            message = ""

            # Try to find the product in the cache database
            cache = products.get_item(self.barcode)
            if cache:
                found = True
                self.name = cache['name']
                tmp = "{} : Found {} from cache"
                tmp = tmp.format(self.barcode, self.name)
                message += tmp+"\n"

            # Try to find the product in the OpenFoodFacts API
            if not found:
                if self.__fetch_openfoodfacts():
                    found = True
                    tmp = "{} : Found {} from OpenFoodFacts"
                    tmp = tmp.format(self.barcode, self.name)
                    message += tmp+"\n"
                else:
                    tmp = "{} : Nothing found on cache nor on OpenFoodFacts."
                    tmp = tmp.format(self.barcode, self.barcode)
                    message += tmp+"\n"

            # Insert into cache
            if found and not cache:
                products.add_item(self.barcode, self.name)
                tmp = "{} : {} added to cache"
                tmp = tmp.format(self.barcode, self.name)
                message += tmp+"\n"

            # Insert in the groceries list
                # If already present, increase quantity by 1

            # Disconnect the database, allowing it to be used by another thread
            db.Connect.off()

            # Print message
            print(message)

    def __fetch_openfoodfacts(self):
        """
        Fetch infos from OpenFoodFacts
        :rtype: bool
        """
        # Fetch
        try:
            url = 'https://world.openfoodfacts.org/api/v0/product/{}.json'
            url = url.format(self.barcode)
            attempt = requests.get(url, timeout=10)
            attempt = attempt.json()
        except Exception as trace:
            return False

        # Do we have a product ?
        if attempt['status'] == 0:
            return False

        # Treat data
        name = ''
        if 'product_name' in attempt['product']:
            name = attempt['product']['product_name']

        if 'brands' in attempt['product']:
            name = name + ' - ' + attempt['product']['brands'].split(',')[0]

        self.name = name
        return True
