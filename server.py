# Server part which stores specific machine data
import socket
import platform
import winreg
import psutil
import sqlite3

#creating a connection to a database
connection = sqlite3.connect('tech_info.db')
cursor = connection.cursor()

# Utworzone więc zakomentowałam

cursor.execute("CREATE TABLE SYSTEM_INFO(SYSTEM, VERSION, MACHINE, BIT_ARCHITECTURE, ENVIRONMENT, HOSTNAME, PROCESSOR)")
cursor.execute("CREATE TABLE SOFTWARE_INFO(INFO1, INFO2, INFO3)")
cursor.execute("CREATE TABLE HARDWARE_INFO(CPU_USAGE_[%], CPU_frequency_[MHz], RAM[GB], HDD_TOTAL_[GB], HDD_USED_[GB], HDD_FREE_[GB], FIRST_USER)")


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
software_info_tuple = (winreg.QueryInfoKey(software))
software_info = str(winreg.QueryInfoKey(software))
winreg.CloseKey(software)


hardware_info = (
    f"CPU USAGE [%]: {psutil.cpu_percent(interval=1)} "
    f"CPU frequency [MHz]: {psutil.cpu_freq().current}"
    f"RAM [GB]: {psutil.virtual_memory()[3]/1000000000} "  # Getting usage of virtual_memory in GB
    f"HDD TOTAL [GB]: {psutil.disk_usage('/').total/1000000000} "
    f"HDD USED [GB]: {psutil.disk_usage('/').used/1000000000} "
    f"HDD FREE [GB]: {psutil.disk_usage('/').free/1000000000} "
    f"USERS : {psutil.users()}"
)
'''
hardware_info = [psutil.cpu_percent(), psutil.cpu_freq(), psutil.virtual_memory()[3] / 1000000000,
                 psutil.virtual_memory()[2], psutil.disk_usage('/').total / 1000000000,
                 psutil.disk_usage('/').used / 1000000000, psutil.disk_usage('/').free / 1000000000
                 ]
'''
# Sending a back message to client
client_socket.send(software_info.encode())
client_socket.send(system_info.encode())
client_socket.send(hardware_info.encode())

#saving info into database
query_system = 'INSERT INTO SYSTEM_INFO VALUES (?, ?, ?, ?, ?, ?, ?)'
query_hardware = 'INSERT INTO HARDWARE_INFO VALUES (?, ?, ?, ?, ?, ?, ?)'
query_software = 'INSERT INTO SOFTWARE_INFO VALUES (?, ?, ?)'
#cursor.execute(query_system, [platform.system(), platform.version(), platform.architecture(),
#                              platform.machine(), platform.node(), platform.processor()])

cursor.execute(query_system, [platform.system(), platform.version(), platform.machine(),
                              platform.architecture()[0], platform.architecture()[1], platform.node(), platform.processor()])
cursor.execute(query_software, [software_info_tuple[0], software_info_tuple[1], software_info_tuple[2]])
cursor.execute(query_hardware, [psutil.cpu_percent(interval=1), str(psutil.cpu_freq().current), psutil.virtual_memory()[3] / 1000000000,
                                psutil.disk_usage('/').total / 1000000000, psutil.disk_usage('/').used / 1000000000, psutil.disk_usage('/').free / 1000000000, psutil.users()[0].name])


connection.commit()
connection.close()


# Closing the connection
client_socket.close()
