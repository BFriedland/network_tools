import socket

# Necessary for accepting CLI arguments:
import sys

import time

import threading


class ClientThread(threading.Thread):

    def __init__(self):

        super(ClientThread, self).__init__()

    def set_up_client(self):


            self.client_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_IP)

            self.address_for_this_process = ('127.0.0.1', 50000)

            self.client_socket.connect(self.address_for_this_process)


    def enlistify_cli_arguments(self):

        # Send all command line arguments through the socket with sendall():

        list_of_arguments = []

        # Skip the first argument because it's just the file name.
        for each_argument_index in range(1, len(sys.argv)):

            list_of_arguments.append(sys.argv[each_argument_index])

        return list_of_arguments

    def send_messages(self, messages, testing=False):

        if testing == True:

            try:

                for each_message in messages:

                    each_message.decode('ascii')

                    each_message.encode('ascii')

                    return each_message

            except UnicodeDecodeError:

                return "Unicode detected, messages not sent\n"

        else:

            # Preempt unicode errors:
            try:

                for each_message in messages:

                    each_message.decode('ascii')

                    self.client_socket.sendall(each_message)

                self.client_socket.shutdown(socket.SHUT_WR)

            except UnicodeDecodeError:

                print("Unicode detected, messages not sent\n")


    def run(self):

        # Preempt errors failing to close the socket:
        try:
            self.set_up_client()
            #self.client_socket = socket.socket(
            #    socket.AF_INET,
            #    socket.SOCK_STREAM,
            #    socket.IPPROTO_IP)

            #address_for_this_process = ('127.0.0.1', 50000)

            #self.client_socket.connect(address_for_this_process)

            # This would be very different if the specs weren't for
            # CLI input only.
            messages_to_send = self.enlistify_cli_arguments()

            self.send_messages(messages_to_send)

        finally:
            # This made me realize there was a more general "ThreadedSocket"
            # class that could be made and subclassed for Client and Server.
            # However, it would take time to refactor it for that and I'd have
            # a whole host of errors to care about.

            # Always close the socket before leaving.
            self.client_socket.close()


class ServerThread(threading.Thread):

    def __init__(self):

        super(ServerThread, self).__init__()


    def set_up_server(self):

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP)

        self.address_for_this_process = ('127.0.0.1', 50000)

        self.server_socket.bind(self.address_for_this_process)

        # The next two lines prepare the server for connections:
        self.server_socket.listen(1)

        self.server_side_connection, self.server_side_client_address \
            = self.server_socket.accept()




    def run(self):

        # Preempt errors failing to close the socket:
        try:
            self.set_up_server()
            #self.server_socket = socket.socket(
            #    socket.AF_INET,
            #    socket.SOCK_STREAM,
            #    socket.IPPROTO_IP)

            #address_for_this_process = ('127.0.0.1', 50000)

            #self.server_socket.bind(address_for_this_process)

            # The next two lines prepare the server for connections:
            #self.server_socket.listen(1)

            #self.server_side_connection, self.server_side_client_address \
            #    = self.server_socket.accept()

            self.data = self.server_side_connection.recv(32)

            print(self.data)

        finally:
            # This made me realize there was a more general "ThreadedSocket"
            # class that could be made and subclassed for Client and Server.
            # However, it would take time to refactor it for that and I'd have
            # a whole host of errors to care about.

            # Always close the socket before leaving.
            self.server_socket.close()


def run_threads():
    server_thread = ServerThread()
    server_thread.start()

    # Hopefully this will be enough of a delay on its own. Otherwise, use:
    # time.sleep()
    # It wasn't enough.
    # time.sleep(2)
    # or was it?
    # No need for sleep! Sleep is for the weak!
    # -- Code Fellows' students' motto

    client_thread = ClientThread()
    client_thread.start()

    server_thread.join()
    client_thread.join()


if __name__ == "__main__":

    run_threads()
