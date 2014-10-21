
import socket
import unittest
import http_server
# sdiehl.github.io/gevent-tutorial
from gevent.server import StreamServer


class test_HTTPServer(unittest.TestCase):

    def setUp(self):

        self.client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP)

        self.client_socket.connect(('127.0.0.1', 50000))

    # All the test_return_x functions test the functions
    # of the HTTPRequestParser, too, as well as handle(),
    # send_message, and run_server(), since the code must
    # run through all of them in order to run these asserts,
    # and the server program must be started to test it.
    def test_return_http_ok(self):

        self.setUp()

        self.client_socket.sendall("GET / HTTP/1.1")
        received_data = self.client_socket.recv(1024)
        self.client_socket.close()

        self.assertEqual(received_data, "HTTP/1.1 200 OK\r\n/\r\n\r\n")

    def test_return_unsupported_version(self):

        self.setUp()

        self.client_socket.sendall("GET / HTTP/0.9")
        received_data = self.client_socket.recv(1024)
        self.client_socket.close()

        self.assertEqual(received_data,
                         "HTTP/0.9 505 HTTP Version Not Supported\r\n\r\n")

    def test_return_method_not_allowed(self):

        self.setUp()

        self.client_socket.sendall("POST / HTTP/1.1")
        received_data = self.client_socket.recv(1024)
        self.client_socket.close()

        self.assertEqual(received_data,
                         "HTTP/1.1 405 Method Not Allowed\r\n\r\n")

    def test_return_error(self):

        self.setUp()

        self.client_socket.sendall("GET/HTTP/1.1")
        received_data = self.client_socket.recv(1024)
        self.client_socket.close()

        self.assertEqual(received_data,
                         "HTTP/0.9 400 Bad request syntax ('GET/HTTP/1.1')"
                         "\r\n\r\n")


unittest.main()
