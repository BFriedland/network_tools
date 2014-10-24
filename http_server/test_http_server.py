
import socket
import unittest
import http_server
# Used for parsing http responses:
import StringIO
# sdiehl.github.io/gevent-tutorial:
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
    # and run_server(), since the code must run through
    # all of them in order to run these asserts, and the
    # server program must be started to test it.
    def test_return_http_ok(self):

        self.setUp()

        self.client_socket.sendall("GET / HTTP/1.1")
        received_data = self.client_socket.recv(1024)
        self.client_socket.close()

        self.assertEqual(received_data, "HTTP/1.1 200 OK\r\nheaders go here\r\n<b>copy of the directory tree goes here</b>")

    def test_return_unsupported_version(self):

        self.setUp()

        self.client_socket.sendall("GET / HTTP/0.9")
        received_data = self.client_socket.recv(1024)
        self.client_socket.close()

        self.assertEqual(received_data,
                         "HTTP/0.9 505 HTTP Version Not Supported\r\n\")

    def test_return_method_not_allowed(self):

        self.setUp()

        self.client_socket.sendall("POST / HTTP/1.1")
        received_data = self.client_socket.recv(1024)
        self.client_socket.close()

        self.assertEqual(received_data,
                         "HTTP/1.1 405 Method Not Allowed\r\n")

    def test_return_error(self):

        self.setUp()

        self.client_socket.sendall("GET/HTTP/1.1")
        received_data = self.client_socket.recv(1024)
        self.client_socket.close()

        self.assertEqual(received_data,
                         "HTTP/0.9 400 Bad request syntax ('GET/HTTP/1.1')"
                         "\r\n")

    def test_return_file_not_found(self):

        self.setUp()

        self.client_socket.sendall("GET /webbranch HTTP/1.1")
        received_data = self.client_socket.recv(1024)
        self.client_socket.close()

        # Omitting the date for now.
        self.assertEqual(received_data[:24], "HTTP/1.1 404 File Not Found ('")

    def test_craft_ok_http_file_response(self):

        # We'll pick it apart with readline from StringIO.
        # That's the only real way to make an automated test to see if
        # the response is actually spread over multiple lines.

        self.setUp()

        self.client_socket.sendall("GET /webroot/sample.txt HTTP/1.1")

        # I hope this can be interpreted as a string...
        received_data = self.client_socket.recv(1024)

        self.client_socket.close()

        # Using similar pattern to the one used by
        # http_server.HTTPRequestParser()
        rfile = StringIO.StringIO(received_data)

        http_code_stringio_file_line = self.rfile.readline()
        date_stringio_file_line = self.rfile.readline()
        content_type_stringio_file_line = self.rfile.readline()
        blank_stringio_file_line = self.rfile.readline()
        doctype_stringio_file_line = self.rfile.readline()

        self.assertEqual(http_code_stringio_file_line,
                         "HTTP/1.1 200 OK")
        self.assertEqual(date_stringio_file_line,
                         "date skipped due to variety")
        self.assertEqual(content_type_stringio_file_line,
                         "text/html; charset=UTF-8")
        self.assertEqual(blank_stringio_file_line, "")
        self.assertEqual(doctype_stringio_file_line,
                         "<!DOCTYPE HTML><html><body>")




        '''
        GET /test404dontsendanythingpl0z HTTP/1.1\r\n
        \r\n
        HTTP/1.1 404 Not Found\r\n
        Date: datetime.now()\r\n
        Content-Type: text/html; charset=UTF-8
        '''

        '''
        GET / HTTP/1.1\r\n
        \r\n
        HTTP/1.1 200 OK\r\n
        Date: datetime.now()\r\n
        Content-Type: text/html; charset=UTF-8

        '''

    def return_ok_http_directory_response(self):






unittest.main()
