import socket

# Smooths out the process of waiting for sockets to communicate:
import select






# Preempt errors failing to close the socket:
try:

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)

    server_address = ('127.0.0.1', 50000)
    server_socket.bind(server_address)

    # The next two lines prepare the server for connections:
    server_socket.listen(1)

    connection, client_address = server_socket.accept()

    #test if server's close() affects client
    server_socket.close()
    '''
    while True:

        data = connection.recv(32)

        if len(data) > 0:

            # Handle EOT signal:

            # ... does EOT exist? Google gave nothing useful except
            # the ascii code; nothing on point for EOT python,
            # handle EOT python, etc.

            # if EOT in data:

            #    print("EOT encountered, stopping server")

            #    break

            # Data is assumed to be unicode from the client.
            # If this assumption can't be relied on, all it needs is
            # a try:except block, like in the client.
            print(data)

            break

        else:

            select.select()
        '''




finally:
    # Always close the socket before leaving.
    server_socket.close()







