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

from flask import session

import models
import controllers
from utils import Database, Lang
from controllers import webapp

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
        self.params = models.Params(autoload=False)
        self.products = models.Products()
        self.groceries = models.Groceries()

        self.params.create_table()
        self.products.create_table()
        self.groceries.create_table()

        # Params : user config
        self.password_raw = 'abcdefg'
        self.password_sha1 = bytearray(self.password_raw, encoding='utf-8')
        self.password_sha1 = hashlib.sha1(self.password_sha1).hexdigest()
        self.params.add_item('user_password', self.password_sha1)
        self.params.add_item('lang', 'en')

        # Products : 1 sample item
        self.products.add_item('1234567890123', 'Lorem Ipsum', True)

        # Groceries : 1 sample item
        self.groceries.add_item('1234567890123', 1)

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
        Tests the access to the "groceries" page.
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
            Database.on() # Previous call has shut db access
            response = app.post('/', data=data, follow_redirects=True)

            Database.on() # Previous call has shut db access
            response = app.get('/groceries')
            assert response.status_code == 200

    def test_api_groceries_list(self):
        """
        Tests the access to the "groceries_list" API method.
        Success conditions :
        - The API can't be accessed without being logged : HTTP 401
        - Returns HTTP 200 when logged with the expected content as JSON
        """
        with webapp.test_client() as app:
            # Tests access without being authenticated
            response = app.get('/api/groceries_list')
            assert response.status_code == 401

            # Tests access while being authenticated
            data = {'password': self.password_raw}
            Database.on() # Previous call has shut db access
            response = app.post('/', data=data, follow_redirects=True)

            # Does the API returns the expected data ?
            Database.on() # Previous call has shut db access
            response = app.get('/api/groceries_list')
            assert response.status_code == 200
            assert set(self.groceries.get_list()) == set(json.loads(response.data).keys())
