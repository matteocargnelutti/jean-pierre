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

        self.barcode = barcode

    def run(self):
        """
        Fetch, gathers, insert product infos.
        Threaded
        """
        with FindProduct.LOCK:
            print("Threaded test : {}".format(self.barcode))
