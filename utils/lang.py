#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

scanner/utils/lang.py
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import os
import json

#-----------------------------------------------------------------------------
# Lang class
#-----------------------------------------------------------------------------
class Lang:
    """
    Internationalization tool.
    Loads messages in a given language and keeps them as object attributes.
    Usage :
    - lang = Lang('en')
    - lang.message_key
    """
    LANG_PATH = 'lang/'
    """ Defines lang files directory """

    def __init__(self, language='en'):
        """
        Loads a lang file's content as class attributes.
        Tries to find given language, falls back to english if needed.
        :param language: language to load (default : en)
        :type language: str
        :rtype: bool
        """
        self.language = language
        self.language = self.language.replace('..', '')
        self.language = self.language.replace('/', '')

        # Path to the "lang" directory
        langfile = Lang.LANG_PATH + self.language + '.json'

        # Is the wanted language available ?
        if not os.path.isfile(langfile):
            langfile = Lang.LANG_PATH + 'en.json' # Load default
            self.language = 'en'

        # Load file
        data = open(langfile, encoding='utf-8').read()
        data = json.loads(data)

        # Load keys as attributes
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def available(cls):
        """
        Returns a list of available languages
        :rtype: list
        """
        available = []
        for langfile in os.listdir(Lang.LANG_PATH):
            if os.path.isfile(Lang.LANG_PATH + langfile):
                available.append(langfile.replace('.json', ''))

        return available
