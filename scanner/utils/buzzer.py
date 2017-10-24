#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

scanner/utils/buzzer.py
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import time

import RPi.GPIO as GPIO

#-----------------------------------------------------------------------------
# Buzzer class
#-----------------------------------------------------------------------------
class Buzzer:
    """
    This class handles :
    - Sends a signal to a buzzer through a GPIO port
    Usage :
    - buzzer = Buzzer(port)
    - buzzer.beep()
    """
    def __init__(self, port=7, duration=0.1):
        """
        Constructor
        :param port: GPIO port on which the buzzer is connected
        :type port: int
        :param duration: Duration of a single buzz
        :type duration: float
        :rtype: Buzzer
        """
        # Set attributes
        self.port = port
        self.duration = 0.1

        # Inits the port
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)

        # Sets the buzzer to off by default
        GPIO.output(self.port, GPIO.HIGH)

    def beep(self):
        """
        Triggers the buzzer
        """
        GPIO.output(self.port, GPIO.LOW) # On
        time.sleep(self.duration) # Wait
        GPIO.output(self.port, GPIO.HIGH) # Off


    def __del__(self):
        """
        Frees the GPIO port
        """
        GPIO.cleanup() # Clean GPIO config
