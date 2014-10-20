import socket
import threading
import BaseHTTPServer
import StringIO
import unittest
import http_server as http


class test_ThreadedHTTPServer(unittest.TestCase):

    def set_up_test_server(self):

        self.test_server_thread = http.ThreadedHTTPServer()

        self.test_server_thread.start()

    def test_200_ok(self):

        self.set_up_test_server()

        test_client_for_200_ok = ThreadedHTTPClient("GET / HTTP/1.1\r\n")

        result_of_running_test = test_client_for_200_ok.run()

        assertEqual(result_of_running_test[:15], "HTTP/1.1 200 OK")

# The ThreadedHTTPClient is only needed for testing the server.
# Because it isn't in the specs and is used exclusively for testing,
# I put it in the testing file.
class ThreadedHTTPClient(threading.Thread):

    """ Return an HTTP client object built on the threading.Thread class.
    Will set up a client and issue HTTP requests via the autocalled run()
    method when this Thread is start()ed. """

    def __init__(self, string_to_test, ip_address='127.0.0.1',
                 port_number=50000):

        super(ThreadedHTTPClient, self).__init__()

        self.ip_address = ip_address
        self.port_number = port_number
        self.string_to_test = string_to_test

    def set_up_client(self):

            self.client_socket = socket.socket(socket.AF_INET,
                                               socket.SOCK_STREAM,
                                               socket.IPPROTO_TCP)

            self.client_socket.connect((self.ip_address, self.port_number))

    def run(self):

        try:

            self.set_up_client()

            print("Got into the try block in run()")

            # First, issue the request to the server to test its response:
            self.client_socket.sendall(self.string_to_test)

            print("Got past sendall")

            # Receive the server's response and store it to return
            # after the socket is closed:
            self.data_to_return = client_socket.recv(1024)

            if self.data_to_return is None:
                print("uhoh, data_to_return is NONE")
            print(self.data_to_return)

            #self.client_socket.sendall("\r\n\r\n")

        finally:

            # Cleaning up the socket after we're done:
            if self.client_socket is not None:

                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()

            return self.data_to_return


unittest.main()
