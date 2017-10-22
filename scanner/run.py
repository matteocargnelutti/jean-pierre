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
from io import BytesIO

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
    last_scan = ''
    empty_scans = 0
    while True:
        # Get an image from the camera
        stream = BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)

        # Scan image for barcodes
        barcodes = pyzbar_decode(pil_image.open(stream))[::-1]
        #print(barcodes)

        # If there is no barcode : clean last scan history every 3 empty scans in a row
        if not barcodes:
            empty_scans += 1
            if empty_scans == 3:
                last_scan = ''
                empty_scans = 0

        # If there is a barcode
        if barcodes:
            # Isolate
            barcode = barcodes[0].data.decode()

            # Break counter of empty scans in a row
            empty_scans = 0

            # Ignore if the item has just been scanned
            if barcode == last_scan:
                print("Ignored: {}".format(barcode))
                continue

            # Add it to history
            last_scan = barcode
            print("Added: {}".format(barcode))

            # Try to find it in cache

            # If not in cache, get it from the APIS
            # ... or should this task be done by another process, in order to avoid clogging this one ?

            # If found : "beep", add it to the groceries list (or increment its quantity)


# Execute
if __name__ == "__main__":
    try:
        main()
    except Warning as trace:
        logging.warning(trace, exc_info=True)
    except Exception as trace:
        logging.error(trace, exc_info=True)
