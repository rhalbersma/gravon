#!/bin/bash

# https://www.gnu.org/software/wget/manual/wget.html

# download all .zip files into a "downloads" directory
wget -m -nd -e robots=off -A "*.zip" -q -P downloads http://www.gravon.de/strados2/files/

# download the StraDoS2 viwer into a "viewer" directory
wget        -e robots=off            -q -P viewer    https://www.gravon.de/webstart/strados2/strados2.jnlp

# download .zip file from Luc Adriaansen which contains Gravon nicknames (to be matched to Gravon database)
#wget                                 -q -P downloads http://members.chello.nl/~l.adriaansen/Bekenden.zip
