# jeanpierre
**[Prototype]** A Raspberry Pi robot helping people to build groceries list.

**Work in progress**

# Hardware used
* Raspberry Pi Zero W
* Raspberry Pi Camera Module V2
* A random *buzzer* module

# Setup
* Please run *install.sh* : `chmod a+x install.sh` then `./install.sh`

# Processes
**Jean-Pierre is made of three separate processes that are meant to run in parallel.**
* **config** : the configuration assistant.
* **scanner** : sub-app that scans the products with the camera.
* **web** : Flask sub-app that handles the web application.

## Manually launch processes
**Processes are automaticaly handled by supervisor. But in case you want to launch it separately :**
* `python jeanpierre.py --do config` : launches the configuration assistant.
* `python jeanpierre.py --do scanner` : launches the scanner.
* `python jeanpierre.py --do web` : launches the web app process in debug mode.
* `gunicorn --bind 0.0.0.0 jeanpierre:webapp` : launches the web app process in production mode.

# Shared parameters
Key | Value
----| -----
`buzzer_on` | Should Jean-Pierre try to use a buzzer ?
`buzzer_port` | On which GPIO port the buzzer is ? 
`camera_res_x` | Camera's resolution : width
`camera_res_y` | Camera's resolution : height
`user_password` | Password for the web interface (cyphered)
`flask_secret_key`| Auto-generated secret key for Flask

* Theses parameters are defined using the config assistant, run : `python assistant.py` directly from the **config** subdirectory.
* They are stored into the **Params** database.

# Software dependencies
## OS
* Raspbian (lite)

## sudo apt-get install ...
* python3-dev
* python3-pip
* python3-picamera
* git
* virtualenv
* libzbar0
* supervisor
* libjpeg8-dev

## pip dependencies (see python_requirements.txt)
* picamera
* pyzbar
* pyzbar[scripts]
* pytest
* requests
* RPi.GPIO
* flask
* gunicorn

# Note 
* A note about camera focus adjustement (and how it could break the camera)