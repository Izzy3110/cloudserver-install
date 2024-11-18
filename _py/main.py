from __future__ import annotations

import random
import time
from os import environ
import os.path
import socket
import sys
import paramiko
from dotenv import load_dotenv
from paramiko.rsakey import RSAKey
from hcloud import Client
from hcloud.images import Image
from hcloud.server_types import ServerType
from hcloud.ssh_keys import SSHKey
from hcloud import locations

load_dotenv('.env')

HCLOUD_API_TOKEN = os.getenv('HCLOUD_API_TOKEN')
username = "root"
password = ""


class SSHManager:
    key = None
    privatekey_filepath = None

    hostname = None
    username = None
    password = None

    connected = False

    def __init__(self, **kwargs):
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if "privatekey_filepath" in kwargs.keys():
            self.privatekey_filepath = kwargs.get('privatekey_filepath', None)
        if "hostname" in kwargs.keys():
            self.hostname = kwargs.get('hostname')
        if "username" in kwargs.keys():
            self.username = kwargs.get('username')
        if "password" in kwargs.keys():
            self.password = kwargs.get('password')

        self.load_private_key()

    def execute_command(self, command):
        try:
            self.client.connect(hostname=self.hostname, username=self.username, pkey=self.key)
            self.connected = True
        except socket.gaierror as se:
            num, error_message = se.args
            print(f"[{num}] {error_message}")

        if self.connected:
            _stdin, _stdout, _stderr = self.client.exec_command(command)
            for line in iter(lambda: _stdout.readline(128), ""):
                print(line.rstrip())
            print(_stdout.readline().rstrip())
            # print(_stdout.read().decode())
            print("'" + _stderr.read().decode().rstrip() + "'")
        self.client.close()

    def load_private_key(self, filename=None):
        if self.privatekey_filepath is not None:
            filename = self.privatekey_filepath
            print(" - loaded from filepath")
        try:
            self.key = RSAKey.from_private_key_file(filename=filename)
        except FileNotFoundError:
            print(f"Key-File does not exist: {private_key_path}")


class HetznerCloud:
    servers = []
    default_location = None

    def __init__(self):
        self.client = Client(token=f"{HCLOUD_API_TOKEN}")  # Please paste your API token here
        for loc in self.client.locations.get_all():
            print(f"{loc.id} {loc.name}")
            if loc.name == "nbg1":
                self.default_location = loc

    def list_servers(self):
        self.servers = self.client.servers.get_all()
        # for server in self.servers:
        #    # print(server.server_type.name)
        #    print(f"{server.id=} {server.name=} {server.status=}")
        #    print(server.public_net.ipv4.ip)
        return self.servers

    def generate_random_string(self, length=10):
        return ''.join(random.choice(self.char_list) for _ in range(length))

    @staticmethod
    def count_char_occurrences(string, char):
        return string.count(char)

    char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', '-']
    generating = False

    def generate_new_servername(self):
        self.generating = False
        generated = False
        server_name = ""
        while not generated:
            if not self.generating:
                self.generating = True
            server_name = cloud_instance.generate_random_string(20)
            count = cloud_instance.count_char_occurrences(server_name, '-')

            if count > 1:
                first_char = True if server_name[0] == "-" else False
                last_char = True if server_name[-1] == "-" else False
                if first_char:
                    pass
                else:
                    if last_char:
                        pass
                    else:
                        generated = True
                        print("ok")
        self.generating = False
        return server_name

    def create_server(self, server_name=None, server_type='cpx11', image_name='debian-12'):
        if server_name is None:
            server_name = self.generate_new_servername()

        response = self.client.servers.create(
            name=server_name,
            server_type=ServerType(name=server_type),
            location=self.default_location,
            image=Image(name=image_name),
            ssh_keys=[self.client.ssh_keys.get_by_name('rsa-key-20180508-E2-1271v3')]
        )
        server = response.server
        print(f"{server.id=} {server.name=} {server.status=}")
        print(f"root password: {response.root_password}")
        return server, response.root_password


def check_first_last_char(string, char):
    if not string:  # Check if the string is empty
        return False
    return string[0] == char or string[-1] == char


def has_double_char(string, char):
    double_char = char * 2
    return double_char in string


current_server = None
cloud_instance = HetznerCloud()

server, root_password = cloud_instance.create_server()
i = 10
while i >= 0:
    print(f"sleeping {i} seconds")
    time.sleep(1)
    i -= 1

SERVERS_DIR = os.path.join(os.path.dirname(__file__), "servers")
if not os.path.isdir(SERVERS_DIR):
    os.makedirs(SERVERS_DIR, exist_ok=True)


def exec_ssh_command(ssh_cmd):
    no_valid_connections_error_ = False
    while not no_valid_connections_error_:
        try:
            ssh_man.execute_command(ssh_cmd)
            no_valid_connections_error_ = False
            break
        except paramiko.ssh_exception.NoValidConnectionsError:
            no_valid_connections_error_ = True
            pass
    return no_valid_connections_error_


if __name__ == '__main__':
    private_key_path = os.path.join(os.getcwd(), "privatekey-1271v3-open.openSSH")
    ssh_man = SSHManager(
        hostname=server.public_net.ipv4.ip,
        username=username,
        privatekey_filepath=private_key_path
    )
    curl_apt = "apt-get update && \
               apt-get install git -y && \
               curl -sSL https://raw.githubusercontent.com/Izzy3110/cloudserver-install/refs/heads/main/download.sh | bash && \
               cd cloudserver-install && \
               bash install.sh"

    NoValidConnectionsError = exec_ssh_command(curl_apt)
    sys.exit(0)
