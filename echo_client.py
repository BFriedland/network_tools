import socket


client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
    socket.IPPROTO_IP)

# This is just localhost; change when crossing machines
client_address = ('127.0.0.1', 50000)

client_socket.connect(client_address)




