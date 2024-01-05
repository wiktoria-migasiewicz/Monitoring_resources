# Client part downloading information about a machine

import socket
import psutil
import winreg
import platform

# Saving info about machine
hardware_info = [psutil.users()[0].name, psutil.cpu_percent(interval=1), str(psutil.cpu_freq().current),
                 psutil.virtual_memory()[3] / 1000000000, psutil.disk_usage('/').total / 1000000000]

system_info = [psutil.users()[0].name, platform.system(), platform.version(), platform.machine(),
               platform.architecture()[0], platform.architecture()[1], platform.node(), platform.processor()]

location = winreg.HKEY_LOCAL_MACHINE
software = winreg.OpenKeyEx(location, r"SOFTWARE\\")
software_info_tuple = winreg.QueryInfoKey(software)
software_info = str(winreg.QueryInfoKey(software))
winreg.CloseKey(software)


def check_state(hard, sys, sof):
    x = True if hard == [psutil.users()[0].name, psutil.cpu_percent(interval=1),
                         str(psutil.cpu_freq().current), psutil.virtual_memory()[3] / 1000000000,
                         psutil.disk_usage('/').total / 1000000000] else False

    y = True if sys == [psutil.users()[0].name, platform.system(), platform.version(), platform.machine(),
                        platform.architecture()[0], platform.architecture()[1], platform.node(), platform.processor()] \
        else False

    key = winreg.HKEY_LOCAL_MACHINE
    soft = winreg.OpenKeyEx(location, r"SOFTWARE\\")
    soft_info = winreg.QueryInfoKey(soft)
    winreg.CloseKey(software)

    z = True if sof == soft_info else False

    return x and y and z


while True:
    if not check_state(hardware_info, system_info, software_info):

        # Creating a client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 12346)  # Server port and address
        client_socket.connect(server_address)

        hardware_info = [psutil.users()[0].name, psutil.cpu_percent(interval=1), str(psutil.cpu_freq().current),
                         psutil.virtual_memory()[3] / 1000000000, psutil.disk_usage('/').total / 1000000000]

        system_info = [psutil.users()[0].name, platform.system(), platform.version(), platform.machine(),
                       platform.architecture()[0], platform.architecture()[1], platform.node(), platform.processor()]

        location = winreg.HKEY_LOCAL_MACHINE
        software = winreg.OpenKeyEx(location, r"SOFTWARE\\")
        software_info_tuple = winreg.QueryInfoKey(software)
        software_info = str(winreg.QueryInfoKey(software))
        winreg.CloseKey(software)

        # Sending a message to the server
        message = "Request for system information"
        client_socket.send(message.encode())

        # Receiving message from the server
        info1 = client_socket.recv(1024)
        info2 = client_socket.recv(1024)

        # Decoding data to a readable format
        decoded_info1 = info1.decode('unicode_escape')
        decoded_info2 = info2.decode('unicode_escape')

        print(f"Message from the server: {decoded_info1}")
        print(f"Message from the server: {decoded_info2}")

        # Closing the connection
        client_socket.close()



