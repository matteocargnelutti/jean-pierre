# jeanpierre
**[Prototype]** A Raspberry Pi robot helping people to build groceries list.

**Work in progress**

# Hardware used
* Raspberry Pi Zero W
* Raspberry Pi Camera Module V2
* A random *buzzer* module

# App parameters
Key | Value
----| -----
`buzzer_on` | Should Jean-Pierre try to use a buzzer ?
`buzzer_port` | On which GPIO port the buzzer is ? 
`camera_res_x` | Camera's resolution : width
`camera_res_y` | Camera's resolution : height
`user_password` | Password for the web interface (cyphered) 

* Theses parameters are defined using the config assistant, run : `python assistant.py` in the **config** subdirectory.

# Note 
* A note about camera focus adjustement (and how it could break the camera)