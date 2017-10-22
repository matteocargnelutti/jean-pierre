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

#-----------------------------------------------------------------------------
# FindProduct class
#-----------------------------------------------------------------------------
class FindProduct(Thread):
    """
    This class handles :
    - Fetch product's from a barcode from the OpenFoodFacts or Ean-Search API
    Usage :
    Note : This class creates its own thread
    """
    LOCK = RLock()
    """ Thread lock """

    def __init__(self, barcode):
        """
        Inits the thread
        :param barcode: EAN-13 Barcode to search
        :type barcode: str
        :rtype: FindProduct
        """
        Thread.__init__(self)

        # Is the barcode valid ?
        if not re.findall(r'[0-9]{13}', barcode):
            raise TypeError('EAN-13 Barcode expected, {}, given.'.format(barcode))

        # Attributes
        self.barcode = barcode
        self.name = ''


    def run(self):
        """
        Fetch, gathers, insert product infos.
        Threaded
        """
        with FindProduct.LOCK:
            # Try to find the product in the cache database

            # Try to find the product in the OpenFoodFacts API
            if self.__fetch_openfoodfacts():
                print(self.barcode+' = '+self.name)
            else:
                print("Product not found")

            # If not found yet, try to find the product in the EAN-CODE database API

            # Insert into cache

            # Insert in the groceries list
                # If already present, increase quantity by 1

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
        if 'product_name' in attempt:
            name = attempt['product_name']

        if 'brands' in attempt:
            name = attempt['brands'].split(',')[0]

        self.name = name
        return True    

