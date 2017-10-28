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
from utils import Database, Lang

#-----------------------------------------------------------------------------
# Tests for : Utils.FindProduct
#-----------------------------------------------------------------------------
class TestFindProduct:
    """
    Tests for the FindProduct tool.
    FindProduct is threaded : hence, we need to keep an eye on database's
    connection status, since a connexion can only be used by a single thread at once !
    """

    def setup_method(self):
        """
        Setup method, creates a dummy database
        """
        # Creates test database
        Database.TEST_MODE = True
        Database.on()
        self.cursor = Database.CURSOR

        # Create tables
        models.Params(autoload=False).create_table()
        models.Products().create_table()
        models.Groceries().create_table()

        # Defaults barcodes
        self.valid_barcode = '3017620424403'
        self.invalid_barcode = '123456789ABCD'

        # Deconnects database to let threads use them
        Database.off()

    def teardown_method(self):
        """
        Cleans up dummy database after each test
        """
        Database.off()
        os.remove(Database.DATABASE_TEST)

    def test_run_valid(self):
        """
        Tests FindProduct process with both valid and invalid inputs
        Success conditions :
        - Valid input : an item has been added to the Products and Groceries databases
        - Invalid input : an "unknown" item has been added to the Products and Groceries databases
        """
        # Launch threads
        thread_valid = utils.FindProduct(self.valid_barcode)
        thread_valid.start()

        thread_invalid = utils.FindProduct(self.invalid_barcode)
        thread_invalid.start()

        thread_valid.join()
        thread_invalid.join()

        # Tests
        groceries = models.Groceries() # Re-opens the DB connexion too, closed by FindProduct
        valid = groceries.get_item(self.valid_barcode)
        invalid = groceries.get_item(self.invalid_barcode)
        assert valid
        assert valid['name'] != '???'
        assert invalid
        assert invalid['name'] == '???'

#-----------------------------------------------------------------------------
# Tests for : Utils.Lang
#-----------------------------------------------------------------------------
class TestLang:
    """
    Tests for the Lang internationalization tool.
    """

    def test_init_valid(self):
        """
        Tests init with a valid language.
        Success conditions :
        - self.language == en
        - self.config_intro exists and is not empty
        """
        lang = Lang()
        assert lang.language == 'en'
        assert lang.config_intro

    def test_init_invalid(self):
        """
        Tests init with a invalid language.
        Success conditions :
        - self.language == en (english fallback)
        - self.config_intro exists and is not empty
        """
        lang = Lang('xxx')
        assert lang.language == 'en'
        assert lang.config_intro

    def test_available(self):
        """
        Tests method that returns list of available languages.
        Success conditions :
        - Returns a list containing at least "en"
        """
        available = Lang.available()
        assert isinstance(available, list)
        assert 'en' in available
