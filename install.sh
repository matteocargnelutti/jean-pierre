#!/bin/bash
#
# Jean-Pierre [Prototype]
# A Raspberry Pi robot that helps people make their grocery list.
# Matteo Cargnelutti - github.com/matteocargnelutti
#
# install.sh - Setup Bash
#

#-----------------------------------------------------------------------------
# Paths
#-----------------------------------------------------------------------------
JEANPIERRE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/;
SUPERVISOR_DIR="/etc/supervisor/conf.d/"

#-----------------------------------------------------------------------------
# Execution rights
#-----------------------------------------------------------------------------
sudo chmod a+x jeanpierre.py;
sudo chmod a+x scanner.sh;
sudo chmod a+x web.sh;
sudo chmod a+x sass.sh;

#-----------------------------------------------------------------------------
# Dystem dependencies
#-----------------------------------------------------------------------------
sudo apt-get install git python3-dev python3-pip python3-picamera virtualenv libzbar0 supervisor libjpeg8-dev build-essential;

#-----------------------------------------------------------------------------
# Virtual env
#-----------------------------------------------------------------------------
virtualenv -p python3 env;
source env/bin/activate; # The virtual env is now activated !
pip install -r requirements.txt;
pip install pyzbar[scripts];

#-----------------------------------------------------------------------------
# Jean-Pierre's config
#-----------------------------------------------------------------------------
clear;
./jeanpierre.py --do config;

#-----------------------------------------------------------------------------
# Supervisor
#-----------------------------------------------------------------------------
# For scanner
$TO_WRITE=$SUPERVISOR_DIR"jeanpierre-scanner.conf"
sudo touch $TO_WRITE;
sudo echo "[program:purbeurre-gunicorn]" >> $TO_WRITE;
sudo echo "command = ."$JEANPIERRE_DIR"scanner.sh" >> $TO_WRITE;
sudo echo "user = $USER" >> $TO_WRITE;
sudo echo "autostart = true" >> $TO_WRITE;
sudo echo "autorestart = true" >> $TO_WRITE;

# For Gunicorn
$TO_WRITE = $SUPERVISOR_DIR"jeanpierre-gunicorn.conf"
sudo touch $TO_WRITE;
sudo echo "[program:purbeurre-gunicorn]" >> $TO_WRITE;
sudo echo "command = ."$JEANPIERRE_DIR"web.sh" >> $TO_WRITE;
sudo echo "user = $USER" >> $TO_WRITE;
sudo echo "autostart = true" >> $TO_WRITE;
sudo echo "autorestart = true" >> $TO_WRITE;

# Init
sudo supervisorctl reread;
sudo supervisorctl update;

#-----------------------------------------------------------------------------
# KTHXBYE
#-----------------------------------------------------------------------------
echo "[:{ End of Jean-Pierre's install script. Please check the output !";