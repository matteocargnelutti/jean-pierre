# jeanpierre
**[Prototype]** A Raspberry Pi robot helping people to build groceries list.

**Work in progress**

# Hardware used
* Raspberry Pi Zero W
* Raspberry Pi Camera Module V2
* A random *buzzer* module

# 3 apps, 1 database
* Jean-Pierre is made of three apps : **config**, **scanner** and **web**
* The three apps share as a SQLite 3 database, stored in `database.db` on the root directory.

# Shared parameters
Key | Value
----| -----
`BUZZER_ON` | Should Jean-Pierre try to use a buzzer ?
`BUZZER_PORT` | On which GPIO port the buzzer is ? 
`CAMERA_RES_X` | Camera's resolution : width
`CAMERA_RES_Y` | Camera's resolution : height
`USER_PASSWORD` | Password for the web interface (cyphered) 

* Theses parameters are defined using the config assistant, run : `python assistant.py` directly from the **config** subdirectory.
* They are stored into the **Params** database.

# Note 
* A note about camera focus adjustement (and how it could break the camera)