#!/bin/bash

# download all .zip files into a "downloads" directory
wget -m -nd -e robots=off -A "*.zip" -q -P downloads http://www.gravon.de/strados2/files/

# download .zip file from Luc Adriaansen which contains Gravon nicknames (to be matched to Gravon database)
#wget                                 -q -P downloads http://members.chello.nl/~l.adriaansen/Bekenden.zip
