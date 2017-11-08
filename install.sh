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

#-----------------------------------------------------------------------------
# Execution rights
#-----------------------------------------------------------------------------
chmod a+x jeanpierre.py;
chmod a+x scanner.sh;
chmod a+x web.sh;
chmod a+x sass.sh;
chmod a+x uninstall.sh;

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
# Please excuse this ugly script :D ...
#-----------------------------------------------------------------------------

# For scanner
TO_WRITE=/etc/supervisor/conf.d/jeanpierre-scanner.conf;
sudo touch $TO_WRITE;
echo "[program:jeanpierre-scanner]" | sudo tee $TO_WRITE > /dev/null;
echo "command = ."$JEANPIERRE_DIR"scanner.sh" | sudo tee --append $TO_WRITE > /dev/null;
echo "user = $USER" | sudo tee --append $TO_WRITE > /dev/null;
echo "autostart = true" | sudo tee --append $TO_WRITE > /dev/null;
echo "autorestart = true" | sudo tee --append $TO_WRITE > /dev/null;

# For Gunicorn
TO_WRITE=/etc/supervisor/conf.d/jeanpierre-web.conf;
sudo touch $TO_WRITE;
echo "[program:jeanpierre-web]" | sudo tee $TO_WRITE > /dev/null;
echo "command = ."$JEANPIERRE_DIR"web.sh" | sudo tee --append $TO_WRITE > /dev/null;
echo "user = $USER" | sudo tee --append $TO_WRITE > /dev/null;
echo "autostart = true" | sudo tee --append $TO_WRITE > /dev/null;
echo "autorestart = true" | sudo tee --append $TO_WRITE > /dev/null;

# Init
sudo supervisorctl reread;
sudo supervisorctl update;

#-----------------------------------------------------------------------------
# KTHXBYE
#-----------------------------------------------------------------------------
echo "[:{ End of Jean-Pierre's install script. ";
echo "Please reboot your Pi in ordrer to let Jean-Pierre boot."