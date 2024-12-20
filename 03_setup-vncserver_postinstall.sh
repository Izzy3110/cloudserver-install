#!/bin/bash

DESTINATION="/root/.vnc/xstartup"
URL="https://raw.githubusercontent.com/Izzy3110/cloudserver-install/refs/heads/main/vncserver/xstartup"

if wget -q -O "$DESTINATION" "$URL"; then
    echo "Download successful! File saved to $DESTINATION."
else
    echo "Download failed!" >&2
    exit 1
fi

mkdir -p $HOME/.local/share/applications
DESKTOP_FILE_PATH="$HOME/.local/share/applications/firefox-esr.desktop"

echo "Creating Firefox desktop launcher..."
cat <<EOF > "$DESKTOP_FILE_PATH"
[Desktop Entry]
Version=1.0
Type=Application
Name=Firefox ESR Web Browser
Comment=Browse the web
Exec=/usr/bin/firefox %u
Icon=/usr/lib/firefox-esr/browser/chrome/icons/default/default128.png
Terminal=false
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;application/xml;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;x-scheme-handler/chrome;application/x-xpinstall;
StartupNotify=true
EOF

chmod +x "$DESKTOP_FILE_PATH"

chmod +x $DESTINATION
vncserver -kill :1
vncserver -geometry 1920x1500
