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
import base64
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
        self.pic = ''


    def run(self):
        """
        Fetch, gathers, insert product infos and adds it to the groceries list.
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
            groceries = db.GroceriesTable()
            message = ""

            # Try to find the product in the local products database
            cache = products.get_item(self.barcode)
            if cache:
                found = True
                self.name = cache['name']
                self.barcode = cache['barcode']
                message += "{} : Found {} from local (cache) database.\n".format(self.barcode, self.name)

            # If not found localy : Try to find the product in the OpenFoodFacts API
            if not found:
                # If found on OpenFoodFacts : add it to the local database
                if self.__fetch_openfoodfacts():
                    found = True
                    products.add_item(self.barcode, self.name, self.pic) 
                    message += "{} : Found {} from OpenFoodFacts.\n".format(self.barcode, self.name)
                    message += "{} : {} added to cache.\n".format(self.barcode, self.name)
                else:
                    message += "{} : Not found localy nor on OpenFoodFacts.\n".format(self.barcode)

            # If found : Update the groceries list with this item
            if found:
                # If the product's already present in the groceries list: increase its quantity by 1
                existing = groceries.get_item(self.barcode)
                if existing:
                    quantity =  existing['quantity'] + 1
                    groceries.edit_item(self.barcode, quantity)
                    message += "{} : {} {} in groceries list.\n".format(self.barcode, quantity, self.name)
                # Otherwise : add it
                else:
                    groceries.add_item(self.barcode, 1)
                    message += "{} : {} added to the groceries list, quantity : 1.\n".format(self.barcode, self.name)

            # Disconnect the database, allowing it to be used by another thread
            db.Connect.off()

            # Print message
            print(message)

    def __fetch_openfoodfacts(self):
        """
        Fetch infos from OpenFoodFacts.
        Automaticaly updates attributes with the results.
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

        # Get image
        if 'image_thumb_url' in attempt['product']:
            thumb = attempt['product']['image_thumb_url']
            try:
                pic = requests.get(thumb, timeout=10)
                self.pic = b"data:image/jpg;base64," + base64.b64encode(pic.content)
            except Exception as trace:
                self.pic = '' # Ignore

        self.name = name
        return True
