#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

models/params.py
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from utils import Database

#-----------------------------------------------------------------------------
# Params Table class
#-----------------------------------------------------------------------------
class Params:
    """
    This class handles :
    - Load and read parameters from the Params table as attributes
    Usage :
    - params = Params()
    - params.PARAM_NAME
    """
    def __init__(self, autoload=True):
        """
        Constructor
        :param autoload: Automaticaly load parameters as attributes ?
        :rtype: ParamsTable
        """
        # Is the database connexion initialized ?
        if not Database.is_ready():
            Database.on()

        # Load parameters as attributes
        if autoload:
            self.load()

    def load(self):
        """
        Load parameters as attributes
        :rtype bool:
        """
        # Get all the parameters
        Database.CURSOR.execute("SELECT * FROM Params;")
        items = Database.CURSOR.fetchall()

        # Store parameters as attributes in lower caps as they are not constants
        if not items:
            return False
        if items:
            for item in items:
                setattr(self, item['key'].lower(), item['value'])
                self.camera_res_x = int(self.camera_res_x)
                self.camera_res_y = int(self.camera_res_y)
                self.buzzer_on = int(self.buzzer_on)
                self.buzzer_port = int(self.buzzer_port)
            return True

    def create_table(self):
        """
        Creates the Params table
        :rtype: bool
        """
        query = """
                CREATE TABLE IF NOT EXISTS Params (
                    [key] TEXT PRIMARY KEY,
                    value TEXT
                )
                WITHOUT ROWID;
                """
        Database.LINK.execute(query)
        Database.LINK.commit()
        return True

    def add_item(self, key, value=""):
        """
        Adds a parameter into the database
        :param key: parameter key
        :param value: parameter value
        :type key: str
        :type value: str
        :rtype: bool
        """
        query = """
                INSERT INTO params VALUES (?, ?)
                """
        params = (key, value)
        Database.LINK.execute(query, params)
        Database.LINK.commit()
        setattr(self, key, value) # Update parameter loaded as attribute
        return True

    def delete_item(self, key):
        """
        Deletes a parameter from the database
        :param key: parameter key
        :type key: str
        :rtype: bool
        """
        # Only if the item exists
        if hasattr(self, key):
            return True

        # Deletion
        query = """
                DELETE FROM params WHERE `key` = ?
                """
        params = (key,)
        Database.LINK.execute(query, params)
        Database.LINK.commit()
        delattr(self, key) # Delete parameter loaded as attribute
        return True
