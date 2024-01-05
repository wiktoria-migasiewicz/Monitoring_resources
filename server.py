# Server part which stores specific machine data

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safety.settings")
django.setup()

from collector.models import SystemInformation, SoftwareInformation, HardwareInformation
from django.db import models

import socket
import platform
import winreg
import psutil
import sqlite3


# Creating a server
server_address = ('localhost', 12346)  # Server port and address

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 and stream socket
server_socket.bind(server_address)
server_socket.listen(1)

while True:
    print("Waiting for a connection...")

    # Accepting a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connected with {client_address}")

    # Decoding data received from client
    data = client_socket.recv(1024).decode()
    print(f"Data received from client: {data}")

    # Defining hardware info from client's machine
    hardware_info = [psutil.users()[0].name, psutil.cpu_percent(interval=1), str(psutil.cpu_freq().current),
                     psutil.virtual_memory()[3] / 1000000000, psutil.disk_usage('/').total / 1000000000]

    # Defining system info from client's machine
    system_info = [psutil.users()[0].name, platform.system(), platform.version(), platform.machine(),
                   platform.architecture()[0], platform.architecture()[1], platform.node(), platform.processor()]

    # Store location of HKEY_LOCAL_MACHINE
    location = winreg.HKEY_LOCAL_MACHINE
    software = winreg.OpenKeyEx(location, r"SOFTWARE\\")
    software_info_tuple = winreg.QueryInfoKey(software)
    software_info = str(winreg.QueryInfoKey(software))
    winreg.CloseKey(software)

    # Checking whether such client already exists in database
    try:
        if SystemInformation.objects.filter(USER=psutil.users()[0].name).exists():

            # Sending a back message to client
            client_socket.send('Checking for updates'.encode())

            # Updating info if needed

            try:
                system_info = SystemInformation.objects.update(
                    USER=psutil.users()[0].name,
                    SYSTEM=platform.system(),
                    VERSION=platform.version(),
                    MACHINE=platform.machine(),
                    ARCHITECTURE=platform.architecture()[0],
                    ENVIRONMENT=platform.architecture()[1],
                    HOSTNAME=platform.node(),
                    PROCESSOR=platform.processor()
                )
                software_info = SoftwareInformation.objects.update(
                    USER=psutil.users()[0].name,
                    INFO1=software_info_tuple[0],
                    INFO2=software_info_tuple[1],
                    INFO3=software_info_tuple[2]
                )
                hardware_info = HardwareInformation.objects.update(
                    USER=psutil.users()[0].name,
                    CPU_USAGE=str(psutil.cpu_percent(interval=1)),
                    CPU_FREQUENCY=str(psutil.cpu_freq().current),
                    RAM=str(psutil.virtual_memory()[3] / 1000000000),
                    HDD_TOTAL=str(psutil.disk_usage('/').total / 1000000000),
                )

                client_socket.send('Updated successfully'.encode())

            except sqlite3.OperationalError:
                client_socket.send('Update failed'.encode())

        else:
            # Sending a back message to client
            client_socket.send('New user'.encode())

            try:

                system_info = SystemInformation.objects.create(
                    USER=psutil.users()[0].name,
                    SYSTEM=platform.system(),
                    VERSION=platform.version(),
                    MACHINE=platform.machine(),
                    ARCHITECTURE=platform.architecture()[0],
                    ENVIRONMENT=platform.architecture()[1],
                    HOSTNAME=platform.node(),
                    PROCESSOR=platform.processor()
                )
                software_info = SoftwareInformation.objects.create(
                    USER=psutil.users()[0].name,
                    INFO1=software_info_tuple[0],
                    INFO2=software_info_tuple[1],
                    INFO3=software_info_tuple[2]
                )
                hardware_info = HardwareInformation.objects.create(
                    USER=psutil.users()[0].name,
                    CPU_USAGE=str(psutil.cpu_percent(interval=1)),
                    CPU_FREQUENCY=str(psutil.cpu_freq().current),
                    RAM=str(psutil.virtual_memory()[3] / 1000000000),
                    HDD_TOTAL=str(psutil.disk_usage('/').total / 1000000000),
                )
                client_socket.send('New user added to database'.encode())
            except sqlite3.OperationalError:
                client_socket.send('Adding to database failed'.encode())

    except sqlite3.OperationalError:
        client_socket.send('Something went wrong'.encode())

    # Closing connections
    client_socket.close()