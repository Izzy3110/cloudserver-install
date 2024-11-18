#!/usr/bin/python3
import subprocess

# Define the command to execute
cmd = "sudo apt-get install git -y; git clone http://github.com/Izzy3110/cloudserver-install"

# Use subprocess to execute the command
with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as ps:
    stdout, stderr = ps.communicate()

# Print the results
print("STDOUT:")
print(stdout)

print("\nSTDERR:")
print(stderr)

# Check the return code
if ps.returncode == 0:
    print("\nCommand executed successfully.")
else:
    print("\nCommand failed with return code:", ps.returncode)

