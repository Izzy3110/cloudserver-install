#!/bin/bash

DESTINATION="/root/.vnc/xstartup"
URL="https://raw.githubusercontent.com/Izzy3110/cloudserver-install/refs/heads/main/vncserver/xstartup"

if wget -O "$DESTINATION" "$URL"; then
    echo "Download successful! File saved to $DESTINATION."
else
    echo "Download failed!" >&2
    exit 1
fi

chmod +x $DESTINATION
vncserver -kill :1
vncserver -geometry 1920x1500
