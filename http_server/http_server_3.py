
import socket

import BaseHTTPServer

import StringIO


# sdiehl.github.io/gevent-tutorial
from gevent.server import StreamServer



def handle(socket, address):

    unparsed_http_request = socket.recv(1024)

    parsed_http_response = HTTPRequestParser(unparsed_http_request)

    # do arg parsing here


    if parsed_http_response.error_code is not None:

        return_error(socket, parsed_http_response)

    elif parsed_http_response.request_version != "HTTP/1.1":

        return_unsupported_version(socket, parsed_http_response)

    elif parsed_http_response.command != "GET":

        return_method_not_allowed(socket, parsed_http_response)

    elif parsed_http_response.error_code is None:

        return_http_ok(socket, parsed_http_response)


    socket.close()

# First, the generic error case:
def return_error(socket, parsed_http_response):
    ''' Implement a function that will return
    a well formed HTTP error response
    (The error code and message should be
    parameterized so that this function
    can be used in a variety of situations).
    The response should be a byte string
    suitable for transmission through a socket. '''

    print("[Sent] %s %s %s\r\n" % (
        parsed_http_response.request_version,
        parsed_http_response.error_code,
        parsed_http_response.error_message))

    # This will return properly formatted
    # requests for all errors.
    socket.sendall("%s %s %s\r\n\r\n" % (
        parsed_http_response.request_version,
        parsed_http_response.error_code,
        parsed_http_response.error_message))


# Second, the version forbidden case:
def return_unsupported_version(socket, parsed_http_response):

    ''' The function should only accept HTTP/1.1
    requests, a request of any other protocol
    should raise an appropriate error '''

    print("[Sent] %s 505 HTTP Version Not Supported\r\n"
          % (parsed_http_response.request_version))

    socket.sendall(
        "%s 505 HTTP Version Not Supported\r\n\r\n"
        % (parsed_http_response.request_version))

# Third, the method forbidden case:
def return_method_disallowed(socket, parsed_http_response):

    ''' The function should only accept GET requests,
    any other request should raise an appropriate error '''

    print("[Sent] %s 405 Method Not Allowed\r\n"
          % (parsed_http_response.command))

    socket.sendall("%s 405 Method Not Allowed\r\n\r\n" %
                            (parsed_http_response.command))

# Fourth, the acceptable request case:
def return_http_ok(socket, parsed_http_response):

    ''' Implement a function that will return
    a well formed HTTP "200 OK" response as
    a byte string suitable for transmission
    through a socket. '''

    # Apparently, "200 OK" is not an error code.
    socket.sendall("%s 200 OK\r\n" %
                            (parsed_http_response.
                             request_version))

    print("[Sent] %s 200 OK" % (parsed_http_response.request_version))

    ''' Implement a function that will parse
    an HTTP request and return the URI requested. '''

    # After the request has been checked, return the URI.
    socket.sendall(parsed_http_response.path + "\r\n\r\n")

    print("[Sent] %s\r\n" % (parsed_http_response.path))







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

http_server = StreamServer(('127.0.0.1', 5000), handle)
http_server.serve_forever()



