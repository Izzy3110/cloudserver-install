#!/bin/bash
PWD=$(pwd)
TARGET_DIR="/home/sascha/install"
cd $TARGET_DIR
wget "https://raw.githubusercontent.com/Izzy3110/cloudserver-install/refs/heads/main/download.sh"
chmod +x download.sh
/bin/bash download.sh

cd cloudserver-install
/bin/bash install.sh

