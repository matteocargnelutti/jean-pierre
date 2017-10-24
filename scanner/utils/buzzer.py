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
        :param duration: Duration of a single buzz
        :type port: int
        :type duration: float
        :rtype: Buzzer
        """
        # Set attributes
        self.port = port
        self.duration = duration

    def beep(self):
        """
        Triggers the buzzer
        """
        # Inits the port
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)

        # Beep
        GPIO.output(self.port, GPIO.LOW) # On
        time.sleep(self.duration) # Wait
        GPIO.output(self.port, GPIO.HIGH) # Off

        # Cleanup
        GPIO.cleanup()
