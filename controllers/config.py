#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot that helps people make their grocery list.
Matteo Cargnelutti - github.com/matteocargnelutti

controllers/config.py - Configuration assistant class
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import random
import string
import re
import hashlib
import getpass

from utils import Database, Lang
import models

#-----------------------------------------------------------------------------
# Config controller class
#-----------------------------------------------------------------------------
class Config:
    """
    This controller class handles:
    - Execution of the configuration prompt
    - Database init
    - User parameters storage
    Usage :
    - controllers.Config.execute()
    """
    @classmethod
    def execute(cls, language='en'):
        """
        Creates database, tables and ask for user parameters.
        :param language: Set language for this menu
        :type language: str
        Defined parameters :
        - buzzer_on
        - buzzer_port
        - camera_res_x
        - camera_res_y
        - user_password
        - lang
        - api_key
        """
        # Language file
        lang = Lang(language)

        # Intro
        print("-"*80)
        print(lang.config_intro)
        print("-"*80)

        # Create / connects to the database
        Database.on()
        print(lang.config_database_created)

        # Create table : params
        params = models.Params(autoload=False)
        params.create_table()
        print(lang.config_table_params_set)

        # Create table : groceries
        groceries = models.Groceries()
        groceries.create_table()
        print(lang.config_table_groceries_set)

        # Create table : products
        products = models.Products()
        products.create_table()
        print(lang.config_table_products_set)

        # Set language
        params.delete_item('lang')
        language = input(lang.config_language_set)
        if language not in Lang.available():
            language = 'en'
        params.add_item('lang', language)

        # Ask for : use buzzer / on which port ?
        params.delete_item('buzzer_on')
        params.delete_item('buzzer_port')
        buzzer_on = input(lang.config_buzzer_on)

        # Yes
        if buzzer_on.upper() == "Y":
            buzzer_port = input(lang.config_buzzer_port)
            if re.findall('([0-9]+)', buzzer_port):
                params.add_item('buzzer_on', '1')
                params.add_item('buzzer_port', buzzer_port)
            else:
                print(lang.config_buzzer_invalid_port)
                params.add_item('buzzer_on', '0')
                params.add_item('buzzer_port', '0')
        # No
        else:
            params.add_item('buzzer_on', '0')
            params.add_item('buzzer_port', '0')

        # Ask for : camera resolution
        params.delete_item('camera_res_x')
        params.delete_item('camera_res_y')

        for axis in ['x', 'y']:
            if axis == 'x':
                question = lang.config_camera_res_x
            else:
                question = lang.config_camera_res_y

            resolution = input(question)
            if not re.findall('([0-9]+)', resolution):
                resolution = 500

            params.add_item('camera_res_{}'.format(axis), resolution)

        # Ask for : user password
        params.delete_item('user_password')
        user_password = getpass.getpass(lang.config_password)
        if not user_password:
            user_password = 'admin'
        user_password = bytearray(user_password, encoding='utf-8')
        user_password = hashlib.sha1(user_password).hexdigest()
        params.add_item('user_password', user_password)

        # Ask for : api key
        params.delete_item('api_key')
        api_key = getpass.getpass(lang.config_api)
        if not api_key:
            api_key = 'fa7369eb-e132-4356-bb3c-29d451310a0f'
        params.add_item('api_key', api_key)

        # Close connection to the database
        Database.off()

        # Bye !
        print(lang.config_done)
