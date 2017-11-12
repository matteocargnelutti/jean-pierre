![logo](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/misc/logo.png)
**Current version :** v0.1 - "Baguette"

[![Build Status](https://travis-ci.org/matteocargnelutti/jean-pierre.svg?branch=master)](https://travis-ci.org/matteocargnelutti/jean-pierre)

# A Raspberry Pi robot that helps people make their grocery list.
**Jean-Pierre** is a little robot based on the **Raspberry Pi Zero W** that uses a **camera** to **scan food barcodes** : it fetches information about the product from the **OpenFoodFacts API** (https://world.openfoodfacts.org/) and adds it to a **grocery list** that the user can manage from a **web interface**.

## What does it look like ?
For now, it just looks like a random Raspberry Pi Zero with a camera module, a buzzer, and a glorious mustache.

![hardware](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/misc/hardware.jpg)

## How does it work ?
*Just place a product in front of Jean-Pierre's camera* : it will detect the barcode and try to find infos about it before adding it to the grocery list.

![beep](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/misc/beep.jpg)

## Web interface
*Jean-Pierre comes with a web interface* that allows users to manage their grocery list and products database from a computer or smartphone.
![software](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/misc/software.png)

# Docs
* [Hardware](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/docs/HARDWARE.md)
* [Setup / Config](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/docs/SETUP.md)
* [User guide](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/docs/USER.md)
* [Dev guide](https://raw.githubusercontent.com/matteocargnelutti/jeanpierre/master/docs/DEV.md)

# Contribute !
I would be glad that *Jean-Pierre* continues to improve and evolve : don't hesitate to contribute :) !

# Special thanks to ...
* My brother *nico_hitman* and *my wife* for their help with the soldering, electronics and everything I am way too clumsy to do.
* *Jako35* for being handsome.
* The authors of all the *awesome libs and APIs* I used in this project.

[@macargnelutti on Twitter](https://twitter.com/macargnelutti)