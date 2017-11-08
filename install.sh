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
# Paths
#-----------------------------------------------------------------------------
JEANPIERRE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/;
SUPERVISOR_DIR="/etc/supervisor/conf.d/"

#-----------------------------------------------------------------------------
# Execution rights
#-----------------------------------------------------------------------------
chmod a+x jeanpierre.py;
chmod a+x daemon-gunicorn.sh;
chmod a+x daemon-scanner.sh;
chmod a+x sass.sh;

#-----------------------------------------------------------------------------
# Dystem dependencies
#-----------------------------------------------------------------------------
apt-get install git python3-dev python3-pip python3-picamera virtualenv libzbar0 supervisor libjpeg8-dev;

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
./jeanpierre.py --do config;

#-----------------------------------------------------------------------------
# Supervisor
#-----------------------------------------------------------------------------
# For scanner
$TO_WRITE = $SUPERVISOR_DIR"jeanpierre-scanner.conf"
touch $TO_WRITE;
echo "[program:purbeurre-gunicorn]" >> $TO_WRITE;
echo "command = ."$JEANPIERRE_DIR"scanner.sh" >> $TO_WRITE;
echo "user = $USER" >> $TO_WRITE;
echo "autostart = true" >> $TO_WRITE;
echo "autorestart = true" >> $TO_WRITE;

# For Gunicorn
$TO_WRITE = $SUPERVISOR_DIR"jeanpierre-gunicorn.conf"
touch $TO_WRITE;
echo "[program:purbeurre-gunicorn]" >> $TO_WRITE;
echo "command = ."$JEANPIERRE_DIR"web.sh" >> $TO_WRITE;
echo "user = $USER" >> $TO_WRITE;
echo "autostart = true" >> $TO_WRITE;
echo "autorestart = true" >> $TO_WRITE;

# Init
supervisorctl reread;
supervisorctl update;

#-----------------------------------------------------------------------------
# KTHXBYE
#-----------------------------------------------------------------------------
echo "[:{ Jean-Pierre is ready !";