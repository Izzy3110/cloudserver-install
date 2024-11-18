#!/bin/bash
/bin/bash 01_apt.sh
STAGE_1=$?
/bin/bash 02_setup-vncserver.sh
STAGE_2=$?
/bin/bash 03_setup-vncserver_postinstall.sh
STAGE_3=$?

echo $STAGE_1
echo $STAGE_2
echo $STAGE_3

