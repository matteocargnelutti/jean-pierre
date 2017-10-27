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

    def test_fetch_openfoodfacts(self):
        """
        Tests the processed return of the OpenFoodFact API
        with both a valid an invalid input.
        These tests run real HTTP requests, not mocks.
        Success conditions :
        - Valid input : data returned
        - Invalid input : no data returned
        """
        # Valid input
        finder = utils.FindProduct(self.valid_barcode)
        found = finder.__fetch_openfoodfacts()
        assert found
        assert finder.barcode == self.valid_barcode
        assert finder.name
        assert finder.pic
        assert finder.quantity == 1

        # Invalid input
        finder = utils.FindProduct(self.invalid_barcode)
        found = finder.__fetch_openfoodfacts()
        assert not found
        assert finder.barcode == self.valid_barcode
        assert not finder.name
        assert not finder.pic
