#! /usr/bin/env python3
# coding: utf-8
"""
Barcode scanning with the picamera
Sandbox #1
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import time

import picamera

#-----------------------------------------------------------------------------
# Test
#-----------------------------------------------------------------------------
# Camera configuration
camera = picamera.PiCamera()

# Get an image
camera.capture('image.jpg')
print("image.jpg written")
