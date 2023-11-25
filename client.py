# Client part
import socket
import psutil

# Creating a client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)  # Server port and address
client_socket.connect(server_address)

# Sending a message to the server
message = "Request for system information"
client_socket.send(message.encode())

software_info = client_socket.recv(1024)
system_info = client_socket.recv(1024)
hardware_info = client_socket.recv(4096)

decoded_sys_info = system_info.decode('unicode_escape')  # Dekodowanie odebranych danych do czytelnego formatu (np. string)
decoded_sof_info = software_info.decode('unicode_escape')
decoded_hdw_info = hardware_info.decode('unicode_escape')

print(f"System info: {system_info}")
print(f"Software info: {software_info}")
print(f"Hardware info: {hardware_info}")

# Closing the connection
client_socket.close()

