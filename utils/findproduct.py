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

from utils import Database
import models

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

    def __init__(self, barcode, is_test=False):
        """
        Inits the thread
        :param barcode: Barcode to search
        :param is_test: Is it a test ?
        :type barcode: str
        :rtype: FindProduct
        """
        Thread.__init__(self)
        self.barcode = barcode
        self.name = ''
        self.pic = ''
        self.quantity = 1
        self.is_test = is_test

    def run(self):
        """
        Fetch, gathers, insert product infos and adds it to the groceries list.
        Threaded
        :rtype: bool
        """
        with FindProduct.LOCK:
            # Database connection
            Database.on(self.is_test)

            # Marks
            found = False
            cache = False
            products = models.Products()
            groceries = models.Groceries()
            message = ""

            # Try to find the product in the local products database
            cache = products.get_item(self.barcode)
            if cache:
                found = True
                self.name = cache['name']
                self.barcode = cache['barcode']
                message += "{barcode} : Found {name} from local products database.\n"

            # If not found locally : Try to find the product in the OpenFoodFacts API
            if not found:
                # If found on OpenFoodFacts : add it to the local database
                if self.__fetch_openfoodfacts():
                    found = True
                    products.add_item(self.barcode, self.name, self.pic)
                    message += "{barcode} : Found {name} from OpenFoodFacts.\n"
                    message += "{barcode} : {name} added to cache.\n"
                else:
                    message += "{barcode} : Not found locally nor on OpenFoodFacts.\n"

            # If found : Update the groceries list with this item
            if found:
                # If the product's already present in the groceries list: increase its quantity by 1
                previous = groceries.get_item(self.barcode)
                if previous:
                    self.quantity = previous['quantity'] + 1
                    groceries.edit_item(self.barcode, self.quantity)
                    message += "{barcode} : {quantity} {name} now in groceries list.\n"
                # Otherwise : add it
                else:
                    groceries.add_item(self.barcode, 1)
                    message += "{barcode} : 1 {name} added to the groceries list.\n"

            # Disconnect the database, allowing it to be used by another thread
            Database.off()

            # Print message
            message = message.format(barcode=self.barcode,
                                     name=self.name,
                                     quantity=self.quantity)
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
