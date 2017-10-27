#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

tests/test_controllers.py - Units tests for the controllers package
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os
import getpass

import models
import controllers
from utils import Database, Lang

#-----------------------------------------------------------------------------
# Tests for : controllers.Config
#-----------------------------------------------------------------------------
class TestConfig:
    """
    Tests for the config controller
    """

    def test_run_valid(self, monkeypatch):
        """
        Tests the configuration assistant with valid parameters.
        Uses a dummy database.
        Success conditions :
        - The database has been created and contains the new data
        """
        # Language
        lang = Lang()

        # Monkeypatch : inputs
        def input_monkeypatched(phrase):
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

        monkeypatch.setitem(__builtins__, 'input', input_monkeypatched)
        monkeypatch.setattr(getpass, 'getpass', input_monkeypatched)

        # Connect to the dummy database
        Database.on(is_test=True)

        # Launch
        controllers.Config.execute()

        # Test
        params = models.Params()
        assert params.buzzer_on == 1
        assert params.buzzer_port == 7
        assert params.camera_res_x == 500
        assert params.camera_res_y == 500
        assert params.user_password
        assert params.flask_secret_key

    def teardown_method(self):
        """
        Cleans up dummy database after each test
        """
        Database.off()
        os.remove(Database.PATH + Database.DATABASE_TEST)
