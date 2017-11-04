#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot that helps people make their grocery list.
Matteo Cargnelutti - github.com/matteocargnelutti

tests/test_controllers.py - Units & integration tests for the controllers package
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os
import getpass
import hashlib
import json

from flask import session

import models
import controllers
from controllers import webapp
from utils import Database, Lang
import utils

#-----------------------------------------------------------------------------
# Tests for : controllers.Config
#-----------------------------------------------------------------------------
class TestConfig:
    """
    Tests for the config controller
    """
    def setup_method(self):
        """
        Setup method. Sets database to test mode
        """
        Database.TEST_MODE = True

    def test_execute_valid(self, monkeypatch):
        """
        Tests the configuration assistant with valid parameters.
        Uses a dummy database.
        Success conditions :
        - The database has been created and contains the new data
        """
        # Language
        lang = Lang()

        # Monkeypatch : inputs
        def input_monkeypatched_valid(phrase):
            """
            Returns what input() should have returned : valid inputs
            """
            if phrase == lang.config_buzzer_on:
                return "Y"

            if phrase == lang.config_buzzer_port:
                return "7"

            if phrase == lang.config_camera_res_x:
                return "500"

            if phrase == lang.config_camera_res_y:
                return "500"

            if phrase == lang.config_password:
                return "1234abcd"

            if phrase == lang.config_language_set:
                return 'en'

        monkeypatch.setitem(__builtins__, 'input', input_monkeypatched_valid)
        monkeypatch.setattr(getpass, 'getpass', input_monkeypatched_valid)

        # Launch
        controllers.Config.execute()

        # Test
        params = models.Params()
        assert params.buzzer_on == 1
        assert params.buzzer_port == 7
        assert params.camera_res_x == 500
        assert params.camera_res_y == 500
        assert params.user_password
        assert params.lang == 'en'

    def test_execute_invalid(self, monkeypatch):
        """
        Tests the configuration assistant with invalid parameters.
        Uses a dummy database.
        Success conditions :
        - The database has been created and contains fallback data
        """
        # Language
        lang = Lang()

        # Monkeypatch : inputs
        def input_monkeypatched_invalid(phrase):
            """
            Returns what input() should have returned : invalid inputs
            """
            if phrase == lang.config_buzzer_on:
                return "Y"

            if phrase == lang.config_buzzer_port:
                return "NaN"

            if phrase == lang.config_camera_res_x:
                return "Foo"

            if phrase == lang.config_camera_res_y:
                return "Bar"

            if phrase == lang.config_password:
                return ""

            if phrase == lang.config_language_set:
                return 'xxx'

        monkeypatch.setitem(__builtins__, 'input', input_monkeypatched_invalid)
        monkeypatch.setattr(getpass, 'getpass', input_monkeypatched_invalid)

        # Launch
        controllers.Config.execute()

        # Test
        params = models.Params()
        assert params.buzzer_on == 0
        assert params.buzzer_port == 0
        assert params.camera_res_x == 500
        assert params.camera_res_y == 500
        assert params.user_password
        assert params.lang == 'en'

    def teardown_method(self):
        """
        Cleans up dummy database after each test
        """
        Database.off()
        os.remove(Database.DATABASE_TEST)

#-----------------------------------------------------------------------------
# Tests for : controllers.Web
#-----------------------------------------------------------------------------
class TestWeb:
    """
    Tests for the web controller, based on flask
    """
    def setup_method(self):
        """
        Setup method :
        - Sets database to test mode and populates it
        - Launches Flask in test mode
        """
        # Database
        Database.TEST_MODE = True
        Database.on()

        # Create test database
        models.Params(autoload=False).create_table()
        models.Products().create_table()
        models.Groceries().create_table()

        # Params : user config
        self.password_raw = 'abcdefg'
        self.password_sha1 = bytearray(self.password_raw, encoding='utf-8')
        self.password_sha1 = hashlib.sha1(self.password_sha1).hexdigest()
        params = models.Params()
        params.add_item('user_password', self.password_sha1)
        params.add_item('lang', 'en')

        # Products : 1 sample item
        self.default_barcode = '1234567890123'
        self.default_name = 'Lorem Ipsum'
        models.Products().add_item(self.default_barcode, self.default_name, True)

        # Groceries : 1 sample item
        models.Groceries().add_item(self.default_barcode, 1)

    def teardown_method(self):
        """
        Cleans up dummy database after each test
        """
        Database.off()
        os.remove(Database.DATABASE_TEST)

    def test_login(self):
        """
        Tests the login process, with both valid and invalid input.
        Success conditions :
        - Valid : HTTP 200, session "is_logged" = True
        - Invalid : HTTP 200, session "is_logged" doesn't exist or is False
        """
        # Invalid
        with webapp.test_client() as app:
            data = {'password': 'xxx'}
            response = app.post('/', data=data, follow_redirects=True)
            assert response.status_code == 200
            assert 'is_logged' not in session or not session['is_logged']

        # Valid
        with webapp.test_client() as app:
            data = {'password': self.password_raw}
            response = app.post('/', data=data, follow_redirects=True)
            assert response.status_code == 200
            assert session['is_logged']

    def test_logout(self):
        """
        Tests the logout process.
        Success conditions :
        - HTTP 200, session "is_logged" doesn't exist anymore
        """
        with webapp.test_client() as app:
            # Log in
            data = {'password': self.password_raw}
            response = app.post('/', data=data, follow_redirects=True)
            assert response.status_code == 200
            assert session['is_logged']

            # Log out
            response = app.get('/logout', follow_redirects=True)
            assert response.status_code == 200
            assert 'is_logged' not in session

    def test_groceries(self):
        """
        Tests access to the "groceries" page.
        Success conditions :
        - The page can't be accessed without being logged (returns HTTP 302)
        - Returns HTTP 200 when logged
        """
        with webapp.test_client() as app:
            # Tests access without being authenticated
            response = app.get('/groceries')
            assert response.status_code == 302

            # Tests access while being authenticated
            data = {'password': self.password_raw}
            response = app.post('/', data=data, follow_redirects=True)

            response = app.get('/groceries')
            assert response.status_code == 200

    def test_api_groceries_list(self):
        """
        Tests the "api_groceries_list" API method.
        Success conditions :
        - The API can't be accessed without being logged : HTTP 401
        - Returns HTTP 200 when logged with the expected content as JSON
        """
        with webapp.test_client() as app:
            # Tests access without being authenticated
            response = app.get('/api/groceries_list')
            assert response.status_code == 401

            # Authenticate
            data = {'password': self.password_raw}
            response = app.post('/', data=data, follow_redirects=True)

            # Does the API returns the expected data ?
            # JSON "item" entry must contain the same thing as Groceries > get_list
            response = app.get('/api/groceries_list')

            expected_data = models.Groceries().get_list()
            given_data = str(response.data, encoding='utf-8')
            given_data = json.loads(given_data)
            given_data = given_data['items'].keys()

            assert response.status_code == 200
            assert set(expected_data) == set(given_data)

    def test_api_groceries_edit(self):
        """
        Tests the "api_groceries_edit" API method.
        Success conditions :
        - The API can't be accessed without being logged : HTTP 401
        - Returns HTTP 200 when logged with the expected content as JSON
        - Perfoms correctly ADD / EDIT / DELETE operations
        """
        with webapp.test_client() as app:
            # Tests access without being authenticated
            response = app.get('/api/groceries_edit/'+self.default_barcode+'/1')
            assert response.status_code == 401

            # Authenticate
            data = {'password': self.password_raw}
            response = app.post('/', data=data, follow_redirects=True)

            # Test : delete, valid input
            response = app.get('/api/groceries_edit/'+self.default_barcode+'/0')
            assert response.status_code == 200
            assert not models.Groceries().get_item(self.default_barcode)

            # Test : add, valid input
            response = app.get('/api/groceries_edit/'+self.default_barcode+'/2')
            entry = models.Groceries().get_item(self.default_barcode)
            assert response.status_code == 200
            assert entry
            assert entry['barcode'] == self.default_barcode
            assert entry['quantity'] == 2

            # Test : edit, valid input
            response = app.get('/api/groceries_edit/'+self.default_barcode+'/4')
            entry = models.Groceries().get_item(self.default_barcode)
            assert response.status_code == 200
            assert entry
            assert entry['barcode'] == self.default_barcode
            assert entry['quantity'] == 4


    def test_products(self):
        """
        Tests access to the "products" page.
        Success conditions :
        - The page can't be accessed without being logged (returns HTTP 302)
        - Returns HTTP 200 when logged
        """
        with webapp.test_client() as app:
            # Tests access without being authenticated
            response = app.get('/products')
            assert response.status_code == 302

            # Tests access while being authenticated
            data = {'password': self.password_raw}
            response = app.post('/', data=data, follow_redirects=True)

            response = app.get('/products')
            assert response.status_code == 200

    def test_api_products_list(self):
        """
        Tests the "api_products_list" API method.
        Success conditions :
        - The API can't be accessed without being logged : HTTP 401
        - Returns HTTP 200 when logged with the expected content as JSON
        """
        with webapp.test_client() as app:
            # Tests access without being authenticated
            response = app.get('/api/products_list')
            assert response.status_code == 401

            # Authenticate
            data = {'password': self.password_raw}
            response = app.post('/', data=data, follow_redirects=True)

            # Does the API returns the expected data ?
            # JSON "item" entry must contain the same thing as Products > get_list
            response = app.get('/api/products_list')

            expected_data = models.Products().get_list()
            given_data = str(response.data, encoding='utf-8')
            given_data = json.loads(given_data)
            given_data = given_data['items'].keys()

            assert response.status_code == 200
            assert set(expected_data) == set(given_data)

    def test_api_products_edit(self):
        """
        Tests the "api_products_edit" API method.
        Success conditions :
        - The API can't be accessed without being logged
        - Perfoms correctly ADD / EDIT  operations
        """
        with webapp.test_client() as app:
            # Tests access without being authenticated
            response = app.get('/api/products_edit/foo/bar')
            assert response.status_code == 401

            # Authenticate
            data = {'password': self.password_raw}
            response = app.post('/', data=data, follow_redirects=True)

            # Test : add
            barcode = '1000000000001'
            name = 'foobar'

            response = app.get('/api/products_edit/'+barcode+'/'+name)
            entry = models.Products().get_item(barcode)
            assert response.status_code == 200
            assert entry
            assert entry['barcode'] == barcode
            assert entry['name'] == name

            # Test : edit
            name = 'barfoo'
            response = app.get('/api/products_edit/'+barcode+'/'+name)
            entry = models.Products().get_item(barcode)
            assert response.status_code == 200
            assert entry
            assert entry['barcode'] == barcode
            assert entry['name'] == name

    def test_api_products_delete(self):
        """
        Tests the "api_products_delete" API method.
        Success conditions :
        - The API can't be accessed without being logged
        - Perfoms correctly DELETE operations
        """
        with webapp.test_client() as app:
            # Tests access without being authenticated
            response = app.get('/api/products_edit/foo/bar')
            assert response.status_code == 401

            # Authenticate
            data = {'password': self.password_raw}
            response = app.post('/', data=data, follow_redirects=True)

            # Test : Delete
            response = app.get('/api/products_delete/'+self.default_barcode)
            assert response.status_code == 200
            assert not models.Products().get_item(self.default_barcode)

    def test_lang(self):
        """
        Tests access to the "lang" JSON content
        Success conditions :
        - Returns HTTP 200 with associated JSON data
        """
        with webapp.test_client() as app:
            response = app.get('/lang')
            
            expected_data = utils.Lang('en').__dict__
            given_data = str(response.data, encoding='utf-8')
            given_data = json.loads(given_data)
            given_data = given_data.keys()

            assert response.status_code == 200
            assert set(expected_data) == set(given_data)
