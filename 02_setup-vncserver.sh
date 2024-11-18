#!/bin/bash
# Default Config Variables
VIEW_ONLY="n" # Change this to "y" if you want a view-only password

# Commandline-Arguments
PASS="${1}"
if [[ ${#PASS} -eq 0 ]]; then
    echo "using default password..."
    PASS="nhzvnc"
fi
VIEW_ONLY_IN="${2}"
VIEW_ONLY_IN_PW="${3}"

# Control-Variables
VIEW_ONLY_SET=0

# Export variables to ENV
export VIEW_ONLY
export PASS

# View-Only Check
if [[ ${#VIEW_ONLY_IN} -gt 0 ]]; then
    if [[ ${#VIEW_ONLY_IN_PW} -eq 0 ]]; then
    	# read VIEW_ONLY_IN_PW from user-input
    	read -p "Enter view-only password: " VIEW_ONLY_IN_PW	
    	export VIEW_ONLY_IN_PW
    fi
    
    VIEW_ONLY="y"
    export VIEW_ONLY
    
    # Change Control-Variable
    VIEW_ONLY_SET=1
fi


if [[ ${VIEW_ONLY,,} == "y" ]]; then
	/usr/bin/expect -c '
	    spawn vncserver
	    expect {
		-nocase "Password:" {
		    send "$env(PASS)\r"
		    exp_continue
		}
		-nocase "Verify:" {
		    send "$env(PASS)\r"
		    exp_continue
		}
		-nocase "Would you like to enter a view-only password (y/n)?" {
		    send "$env(VIEW_ONLY)\r"
		    exp_continue
		}
	    }
	'
elif [[ ${VIEW_ONLY,,} == "n" ]]; then
	
	/usr/bin/expect -c '
	    spawn vncserver
	    expect {
		-nocase "Password:" {
		    send "$env(PASS)\r"
		    exp_continue
		}
		-nocase "Verify:" {
		    send "$env(PASS)\r"
		    exp_continue
		}
		-nocase "Would you like to enter a view-only password (y/n)?" {
		    send "$env(VIEW_ONLY)\r"
		    exp_continue
		}
		-nocase "Password:" {
		    send "$env(VIEW_ONLY_IN_PW)\r"
		    exp_continue
		}
		-nocase "Verify:" {
		    send "$env(VIEW_ONLY_IN_PW)\r"
		    exp_continue
		}
	    }
	'
else
    echo "Invalid input."
fi
