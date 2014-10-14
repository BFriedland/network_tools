import socket


server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
    socket.IPPROTO_IP)

server_address = ('127.0.0.1', 50000)
server_socket.bind(server_address)

# The next two lines prepare the server for connections:
server_socket.listen(1)

connection, client_address = server_socket.accept()
