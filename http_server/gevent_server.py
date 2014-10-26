
import socket
# For easy parsing of the HTTP requests:
import BaseHTTPServer
# Helps BaseHTTPServer:
import StringIO
# sdiehl.github.io/gevent-tutorial:
from gevent.server import StreamServer

import http_server_helper


def handle(socket, address):

    unparsed_data = socket.recv(1024)
    parsed_http_response = HTTPRequestParser(unparsed_data)

    # Message formatting and message sending are separated for ease of testing.

    if parsed_http_response.error_code is not None:
        server_response = http_server_helper.return_error(parsed_http_response)
        socket.send(server_response)

    elif parsed_http_response.request_version != "HTTP/1.1":
        server_response = http_server_helper.return_unsupported_version(
            parsed_http_response)
        socket.send(server_response)

    elif parsed_http_response.command != "GET":
        server_response = http_server_helper.return_method_not_allowed(
            parsed_http_response)
        socket.send(server_response)

    elif parsed_http_response.error_code is None:
        # note to self: feed the returns from
        # return_requested_file_or_directory()
        # into a response crafter which does header creation.
        server_response = \
            http_server_helper.return_ok_http_file_or_directory_response(
                parsed_http_response)
        socket.send(server_response)

    socket.close()


class HTTPRequestParser(BaseHTTPServer.BaseHTTPRequestHandler):

    """ Return an object that contains variables for interpreting
    the pieces of the http_request it is provided as a parameter. """

    # I read about this part of the standard library here:
    # http://stackoverflow.com/questions/4685217/parse-raw-http-headers

    def __init__(self, http_request):

        # Every variable and method name in this class is directly from
        # BaseHTTPRequestHandler itself.
        # They are being set and called in the poorly-interfaced manner
        # BaseHTTPRequestHandler requires.

        self.rfile = StringIO.StringIO(http_request)
        self.raw_requestline = self.rfile.readline()

        # This merely ensures it returns None if no error has been found.
        # Actual error info fills these slots when found.
        self.error_code = None
        self.error_message = None

        # This turns all the raw_requestline calls into a dictionary of
        # mechanically separated HTTP request and header information.
        self.parse_request()

    # This function must be re-defined here to prevent BaseHTTPRequestHandler
    # from attempting to send the error back to its nonexistent client.
    # This is because we're using HTTPRequestParser to handle parsing
    # of HTTP requests without letting it handle too much of the process.
    # In other circumstances this might be done to analyze the request
    # or log it or some such thing.
    def send_error(self, error_code, error_message):

        self.error_code = error_code
        self.error_message = error_message


def run_server():
    http_server = StreamServer(('127.0.0.1', 50000), handle)
    http_server.serve_forever()


if __name__ == "__main__":

    run_server()
