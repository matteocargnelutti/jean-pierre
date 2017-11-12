![logo](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/misc/ban.png)
# Docs : User guide
-- [**Back to README**](http://github.com/matteocargnelutti/jeanpierre)

**Theses instructions assumes that you have followed the following guides :**
* [Hardware](https://github.com/matteocargnelutti/jean-pierre/blob/master/docs/HARDWARE.md)
* [Setup / Config](https://github.com/matteocargnelutti/jean-pierre/blob/master/docs/SETUP.md)

# Scanner
## How to use it ?
**Simply place a product in front of Jean-Pierre's camera :** it will scan its barcode and add it to the grocery list.

![beep](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/misc/beep.jpg)

**If you've plugged a buzzer module on Jean-Pierre**, it will ring it everytime it recognizes a barcode.

To add a similar item multiple times in the grocery list, simply scan it multiple times.

**Unknown items will also be added to the grocery list :** you can then tell Jean-Pierre what it is from the web interface.

## How does it work ?
**When running, Jean-Pierre constantly captures and analyse pictures to try to find barcodes :** given the limited power of the **Pi Zero** it can only do this operation once every ~0.6 seconds.

If it does find an **EAN-13 barcode**, it will ask the [**OpenFoodFacts API**](https://world.openfoodfacts.org/) for info about it, store its name and picture in the local database and add it to the grocery list.

**This process is launched in a separate thread :** hence you can scan multiple product without having to wait for Jean-Pierre to have finished fetching info about a product.

# Web interface
## What can the web interface do ?
![software](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/misc/software.png)

**Grocery list management :**
* Edit quantities
* Remove items
* Manually add an item
* Export the grocery list in a raw format

**Products database management :**
* Add new products
* Edit products
* Set a name for unknown products

All these features are accessible, once logged, by using the main menu available on the right side of the screen.

## How to use it ?
Once it is launched, access it via your **desktop or mobile** browser by **using your Raspberry Pi local IP and the 8000 port as an address**.

**Example** : `http://192.168.0.10:8000`

**You will then land on this page, asking for your password : **
![desktop](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/misc/desktop.png)

## How does it work ?
The web interface uses **Flask as a web** framework and **Gunicorn as a web server**.

It shares the same database than the scanner process.

## A note on security
**Please note that this interface is not meant to be accessible from the internet** : you should only run it on your local network, as it doesn't use **HTTPS** and only uses a **single password** to grant access to the web interface.

You might want to consider making it accessible remotely with an **https connexion and a strong password, or through a proxy** : this documentation will not cover theses aspects for now.

-- [**Next : Dev guide**](https://github.com/matteocargnelutti/jean-pierre/blob/master/docs/DEV.md)