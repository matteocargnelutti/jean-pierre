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
sudo chmod a+x jeanpierre.py;
sudo chmod a+x scanner.sh;
sudo chmod a+x web.sh;
sudo chmod a+x sass.sh;

#-----------------------------------------------------------------------------
# Supervisor
#-----------------------------------------------------------------------------
sudo supervisorctl stop jeanpierre-web;
sudo supervisorctl stop jeanpierre-scanner;
sudo rm /etc/supervisor/conf.d/jeanpierre-web.conf;
sudo rm /etc/supervisor/conf.d/jeanpierre-scanner.conf;
sudo supervisor reread;
sudo supervisor update;

#-----------------------------------------------------------------------------
# Info
#-----------------------------------------------------------------------------
echo "Jean-Pierre's services erased : you can now safely remove its directory."