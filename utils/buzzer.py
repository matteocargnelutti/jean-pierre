#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot that helps people make their grocery list.
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
        self.port = int(port)
        self.duration = duration

    def beep(self, times=1):
        """
        Triggers the buzzer.
        The GPIO setup is made everytime in order to avoid clogging one of them
        in case of hard exit.
        :param times: How many times does the buzzer has to beep ?
        :type times: int
        """
        # Inits the port
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)

        # Beep
        for i in range(0, times):
            GPIO.output(self.port, GPIO.LOW) # On
            time.sleep(self.duration) # Wait
            GPIO.output(self.port, GPIO.HIGH) # Off
            if i < times: # Add a sleep in case of multiple beeps
                time.sleep(self.duration)

        # Cleanup
        GPIO.cleanup()
