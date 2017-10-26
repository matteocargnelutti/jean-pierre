# jeanpierre
**[Prototype]** A Raspberry Pi robot helping people to build groceries list.

**Work in progress**

# Hardware used
* Raspberry Pi Zero W
* Raspberry Pi Camera Module V2
* A random *buzzer* module

# Setup
* Please run *install.sh* : `chmod a+x install.sh` then `./install.sh`

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