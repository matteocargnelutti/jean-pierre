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
        """
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
        # Database init function to be launched at init by the thread
        def init_db():
            Database.on(memory_mode=True)
            models.Params(autoload=False).create_table()
            models.Products().create_table()
            models.Groceries().create_table()
            return True

        utils.FindProduct.init_db = init_db()

        # Valid input
        thread_valid = utils.FindProduct(self.valid_barcode, memory_mode=True)
        thread_valid.start()
        thread_valid.join()
        assert self.groceries.get_item(self.valid_barcode)

        # Invalid input
        thread_invalid = utils.FindProduct(self.invalid_barcode, memory_mode=True)
        thread_invalid.start()
        thread_invalid.join()
        assert not self.groceries.get_item(self.invalid_barcode)
