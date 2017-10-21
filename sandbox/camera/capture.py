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

from pyzbar.pyzbar import decode as pyzbar_decode
from PIL import Image as pyzbar_image

#-----------------------------------------------------------------------------
# Test
#-----------------------------------------------------------------------------
# Camera setup
camera = picamera.PiCamera()
camera.sharpness = 100
camera.brightness = 55
#camera.ISO = 800
camera.resolution = (600, 600)

# Get an image
camera.capture('image.jpg')
