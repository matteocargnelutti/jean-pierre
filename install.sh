#!/bin/bash
#
# Jean-Pierre [Prototype]
# A Raspberry Pi robot that helps people make their grocery list.
# Matteo Cargnelutti - github.com/matteocargnelutti
#
# install.sh - Setup Bash
# [!] This script must be executed with root privileges.
#

#-----------------------------------------------------------------------------
# Define paths
#-----------------------------------------------------------------------------
JEANPIERRE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/;
SUPERVISOR_DIR="/etc/supervisor/conf.d/"

#-----------------------------------------------------------------------------
# Make scripts executable
#-----------------------------------------------------------------------------
chmod a+x jeanpierre.py;

#-----------------------------------------------------------------------------
# Install system dependencies
#-----------------------------------------------------------------------------
apt-get install git python3-dev python3-pip python3-picamera virtualenv libzbar0 supervisor libjpeg8-dev;

#-----------------------------------------------------------------------------
# VIRTUALENV : Create, launch and configure
#-----------------------------------------------------------------------------
virtualenv -p python3 env;
source env/bin/activate; # The virtual env is now activated !
pip install -r requirements.txt;
pip install pyzbar[scripts];

#-----------------------------------------------------------------------------
# CONFIG : Launch project configuration assistant
#-----------------------------------------------------------------------------
./jeanpierre.py --do config;

#-----------------------------------------------------------------------------
# Prepare supervisor tasks
#-----------------------------------------------------------------------------
# For scanner
#touch $SUPERVISOR_DIR"jeanpierre-scanner.conf";
