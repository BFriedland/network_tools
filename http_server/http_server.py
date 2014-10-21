
import socket
import BaseHTTPServer
import StringIO
# sdiehl.github.io/gevent-tutorial
from gevent.server import StreamServer


def handle(socket, address):

    unparsed_data = socket.recv(1024)
    parsed_http_response = HTTPRequestParser(unparsed_data)

    # Message formatting and message sending are separated for ease of testing.

    if parsed_http_response.error_code is not None:
        server_response = return_error(parsed_http_response)
        send_message(socket, server_response)

    elif parsed_http_response.request_version != "HTTP/1.1":
        server_response = return_unsupported_version(parsed_http_response)
        send_message(socket, server_response)

    elif parsed_http_response.command != "GET":
        server_response = return_method_not_allowed(parsed_http_response)
        send_message(socket, server_response)

    elif parsed_http_response.error_code is None:
        server_response = return_http_ok(parsed_http_response)
        send_message(socket, server_response)

    socket.close()


def send_message(socket, message):

    socket.send(message)


# First, the generic error case:
def return_error(parsed_http_response):
    ''' Implement a function that will return
    a well formed HTTP error response
    (The error code and message should be
    parameterized so that this function
    can be used in a variety of situations).
    The response should be a byte string
    suitable for transmission through a socket. '''

    # This will return properly formatted
    # requests for all errors.
    return "%s %s %s\r\n\r\n" % (
        parsed_http_response.request_version,
        parsed_http_response.error_code,
        parsed_http_response.error_message)


# Second, the version forbidden case:
def return_unsupported_version(parsed_http_response):

    ''' The function should only accept HTTP/1.1
    requests, a request of any other protocol
    should raise an appropriate error '''

    return "%s 505 HTTP Version Not Supported\r\n\r\n" \
        % (parsed_http_response.request_version)


# Third, the method forbidden case:
def return_method_not_allowed(parsed_http_response):

    ''' The function should only accept GET requests,
    any other request should raise an appropriate error '''

    return "%s 405 Method Not Allowed\r\n\r\n" \
        % (parsed_http_response.request_version)


# Fourth, the acceptable request case:
def return_http_ok(parsed_http_response):

    ''' Implement a function that will return
    a well formed HTTP "200 OK" response as
    a byte string suitable for transmission
    through a socket. '''

    # Apparently, "200 OK" is not an error code.
    return "%s 200 OK\r\n%s\r\n\r\n" % (parsed_http_response.request_version,
                                        parsed_http_response.path)


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
