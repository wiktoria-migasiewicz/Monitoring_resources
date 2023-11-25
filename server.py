# Server part which stores specific machine data
import socket
import platform
import winreg
import psutil
import sqlite3

# Creating a server
server_address = ('localhost', 12345)  # Server port and address

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(1)

print("Waiting for a connection...")

# Accepting a connection
client_socket, client_address = server_socket.accept()
print(f"Connected with {client_address}")

data = client_socket.recv(1024).decode()
print(f"Data received from client: {data}")

system_info = (
    f"System: {platform.system()} "
    f"Version: {platform.version()} "
    f"Architecture: {platform.architecture()} "
    f"Machine: {platform.machine()} "
    f"Hostname: {platform.node()} "
    f"Processor: {platform.processor()}"
)

# Store location of HKEY_LOCAL_MACHINE
location = winreg.HKEY_LOCAL_MACHINE
software = winreg.OpenKeyEx(location, r"SOFTWARE\\")
software_info = str(winreg.QueryInfoKey(software))
winreg.CloseKey(software)

hardware_info = (
    f"CPU USAGE [%]: {psutil.cpu_percent()} "
    f"CPU frequency [MHz]: {psutil.cpu_freq()}"
    f"RAM [GB]: {psutil.virtual_memory()[3]/1000000000} "  # Getting usage of virtual_memory in GB
    f"RAM [%]: {psutil.virtual_memory()[2]} "  # Getting % usage of virtual_memory
    f"HDD TOTAL [GB]: {psutil.disk_usage('/').total/1000000000} "
    f"HDD USED [GB]: {psutil.disk_usage('/').used/1000000000} "
    f"HDD FREE [GB]: {psutil.disk_usage('/').free/1000000000} "
    f"USERS : {psutil.users()}"
)

# Sending a back message to client
client_socket.send(software_info.encode())
client_socket.send(system_info.encode())
client_socket.send(hardware_info.encode())

#creating a connection to a database
connection = sqlite3.connect('tech_info.db')


# Closing the connection
client_socket.close()
