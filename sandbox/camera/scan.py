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
camera = picamera.PiCamera()
camera.capture('image.jpg')
print("Image.jpg written")
