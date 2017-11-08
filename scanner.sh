#!/bin/bash
#
# Jean-Pierre [Prototype]
# A Raspberry Pi robot that helps people make their grocery list.
# Matteo Cargnelutti - github.com/matteocargnelutti
#
# scanner.sh - Launches the scanner
# [!] This script is meant to be executed by supervisor
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
cd $DIR;
source env/bin/activate;
./jeanpierre.py --do scanner;