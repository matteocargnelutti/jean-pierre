#! /usr/bin/env python3
# coding: utf-8
"""
Jean-Pierre [Prototype]
A Raspberry Pi robot that helps people make their grocery list.
Matteo Cargnelutti - github.com/matteocargnelutti

controllers/scanner.py - Barcode scanner
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from io import BytesIO
import os

if not os.environ.get('PC_MODE'):
    import picamera
    from pyzbar.pyzbar import decode as pyzbar_decode
    from PIL import Image as pil_image

from utils import Database
import utils
import models

#-----------------------------------------------------------------------------
# Scanner controller class
#-----------------------------------------------------------------------------
class Scanner:
    """
    This controller class handles:
    - Barcode scanning from camera's stream
    - Products fetching through FindProduct
    Usage :
    - controllers.Scanner.execute()
    """
    @classmethod
    def execute(cls):
        """
        This method constantly tries to catch barcodes from the camera :
        if it does, search for info and add it to the user's grocery list.
        """
        # Intro
        print("-"*80)
        print("[:{ Jean-Pierre's Barcode Scanner : Running")
        print("-"*80)

        # Database connection
        Database.on()

        # Load parameters
        params = models.Params()

        # Database : end connection
        # (open it only when needed because this program is meant to be shutdown harshly)
        Database.off()

        # Camera setup
        camera = picamera.PiCamera()
        camera.sharpness = 100
        camera.brightness = 50
        camera.contrast = 25
        camera.resolution = (params.camera_res_x, params.camera_res_y)
        camera.start_preview()

        # Double beep to inform the user that Jean-Pierre is ready
        if params.buzzer_on:
            buzzer = utils.Buzzer(params.buzzer_port)
            buzzer.beep(2)

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

                # Break count of empty scans in a row
                empty_scans = 0

                # Ignore the next instructions if the item has just been scanned
                if barcode == last_scan:
                    continue

                # Add it to history
                last_scan = barcode
                print("Scanned and considered : {}".format(barcode))

                # Beep !
                if params.buzzer_on:
                    buzzer.beep()

                # Analyze it in a separate thread
                utils.FindProduct(barcode).start()
