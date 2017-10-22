#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot helping people to build groceries list.
Matteo Cargnelutti - github.com/matteocargnelutti

scanner/run.py - Scanner embed app.
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import logging
import os
import sqlite3

import picamera
from pyzbar.pyzbar import decode as pyzbar_decode
from PIL import Image as pil_image

import database as db

#-----------------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------------
def main():
    """
    Constantly tries to catch barcodes from the camera :
    if it does, search for info and add it to the user's groceries list.
    """
    # Intro
    print("-"*80)
    print("Jean-Pierre Scanner : Running :{o")
    print("-"*80)

    # Database connection
    db.Connect.on()

    # Load parameters
    params = db.ParamsTable()

    # Database : end connection 
    # (open it only when needed because this program is meant to be shutdown harshly)
    db.Connect.off()

    # Camera setup
    camera = picamera.PiCamera()
    camera.sharpness = 100
    camera.brightness = 55
    camera.resolution = (params.camera_res_x,
                         params.camera_res_y)
    camera.start_preview()

    # Capture loop
    while True:
        # Get an image from the camera
        stream = BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)

        # Scan image for barcodes
        barcodes = pyzbar_decode(pil_image.open(stream))[::-1]
        print(barcodes)

# Execute
if __name__ == "__main__":
    try:
        main()
    except Warning as trace:
        logging.warning(trace, exc_info=True)
    except Exception as trace:
        logging.error(trace, exc_info=True)
