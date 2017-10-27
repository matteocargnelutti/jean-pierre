#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

tests/test_utils.py - Units tests for the utils package
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os

import models
import utils
from utils import Database

#-----------------------------------------------------------------------------
# Tests for : Utils.FindProduct
#-----------------------------------------------------------------------------
class TestFindProduct:
    """
    Tests for the FindProduct tool.
    This tool is threaded.
    """

    def setup_method(self):
        """
        Setup method
        Creates a dummy database
        """
        # Creates database
        Database.on(memory_mode=True)
        self.cursor = Database.CURSOR

        # Create tables
        self.params = models.Params(autoload=False)
        self.products = models.Products()
        self.groceries = models.Groceries()
        self.params.create_table()
        self.products.create_table()
        self.groceries.create_table()

        # Defaults
        self.valid_barcode = '3017620424403'
        self.invalid_barcode = '123456789ABCD'

    def test_run_valid(self):
        """
        Tests FindProduct process with both valid and invalid inputs
        Success conditions :
        - Valid input : an item has been added to the Products and Groceries databases
        - Invalid input : no item has been added to the Products nor the Groceries databases
        """
        # Valid input
        thread = utils.FindProduct(self.valid_barcode).start()
        thread.join()
        assert self.groceries.get_item(self.valid_barcode)

        # Invalid input
        thread = utils.FindProduct(self.invalid_barcode).start()
        thread.join()
        assert not self.groceries.get_item(self.invalid_barcode)
