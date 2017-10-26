#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

scanner/database/groceries.py
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from utils import Database

#-----------------------------------------------------------------------------
# Groceries Table class
#-----------------------------------------------------------------------------
class Groceries:
    """
    This class handles :
    - Manages and interacts with the Groceries table, 
    which uses entries from Products to handle a groceries list.
    Usage :
    - groceries = Groceries()
    - groceries_list = groceries.get_list()
    """
    def __init__(self):
        """
        Constructor
        :rtype: GroceriesTable
        """
        # Is the database connexion initialized ?
        if not Database.is_ready():
            Database.on()

    def create_table(self):
        """
        Creates the Groceries table
        :rtype: bool
        """
        query = """
                CREATE TABLE IF NOT EXISTS Groceries (
                    barcode  CHAR (13) PRIMARY KEY,
                    quantity INT
                )
                WITHOUT ROWID;
                """
        Database.LINK.execute(query)
        Database.LINK.commit()
        return True

    def get_item(self, barcode):
        """
        Get an item by barcode + associated name and pic
        :param barcode: barcode of the product to search
        :type barcode: string
        :rtype: dict or false
        """
        query = """
                SELECT 
                    Groceries.*, Products.name, Products.pic 
                FROM 
                    Groceries
                INNER JOIN 
                    Products
                ON 
                    Groceries.barcode = Products.barcode
                WHERE
                    Groceries.barcode = ?
                ORDER BY 
                    Products.name ASC;
                """
        params = (barcode,)

        Database.CURSOR.execute(query, params)
        product = Database.CURSOR.fetchone()

        if product:
            return {
                'barcode': product['barcode'],
                'name': product['name'],
                'quantity': product['quantity'],
                'pic': product['pic']
            }
        else:
            return False

    def add_item(self, barcode, quantity=1):
        """
        Adds an item to the groceries list
        :param barcode: barcode
        :param quantity: quantity
        :type barcode: str
        :type quantity: int
        :rtype: bool
        """
        query = "INSERT INTO Groceries VALUES (?, ?);"
        params = (barcode, quantity)
        Database.LINK.execute(query, params)
        Database.LINK.commit()
        return True

    def edit_item(self, barcode, quantity):
        """
        Edits an item from the groceries list
        :param barcode: barcode
        :param quantity: quantity
        :type barcode: str
        :type quantity: int
        :rtype: bool
        """
        query = "UPDATE Groceries SET quantity = ? WHERE barcode = ?;"
        params = (quantity, barcode)
        Database.LINK.execute(query, params)
        Database.LINK.commit()
        return True

    def delete_item(self, barcode):
        """
        Deletes an item from the groceries list
        :param barcode: barcode
        :param quantity: quantity
        :type barcode: str
        :type quantity: int
        :rtype: bool
        """
        query = "DELETE FROM Groceries WHERE barcode = ?;"
        params = (barcode,)
        Database.LINK.execute(query, params)
        Database.LINK.commit()
        return True

    def get_list(self):
        """
        Gets the groceries list, with associated product data
        :rtype: list of dict
        """
        # Query
        query = """
                SELECT 
                    Groceries.*, Products.name, Products.pic 
                FROM 
                    Groceries
                INNER JOIN 
                    Products
                ON 
                    Groceries.barcode = Products.barcode
                ORDER BY 
                    Products.name ASC;
                """
        Database.CURSOR.execute(query)
        raw_list = Database.CURSOR.fetchall()

        # Prepare return format
        groceries = {}
        for product in raw_list:
            groceries[product['barcode']] = {
                'name': product['name'],
                'quantity': product['quantity'],
                'pic': product['pic']
            }
        return groceries
