import socket

# Necessary for accepting CLI arguments:
import sys


def send_messages(messages):

    # Preempt unicode errors:
    try:

        for each_message in messages:

            each_message.decode('ascii')

            client_socket.sendall(each_message)

        client_socket.shutdown(socket.SHUT_WR)

    except UnicodeDecodeError:
        print "Unicode detected, messages not sent\n"


# Preempt errors failing to close the socket:
try:

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)

    # This is just localhost; change when crossing machines
    client_address = ('127.0.0.1', 50000)

    client_socket.connect(client_address)

    # Send all command line arguments through the socket with sendall():

    list_of_arguments = []

    # Skip the first argument because it's just the file name.
    for each_argument_index in range(1, len(sys.argv)):

        list_of_arguments.append(sys.argv[each_argument_index])


    send_messages(list_of_arguments)


finally:
    # Always close the socket before leaving.
    client_socket.close()
