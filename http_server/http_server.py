
import socket

import threading

import BaseHTTPServer

import StringIO


class ThreadedHTTPServer(threading.Thread):

    """ Return an HTTP server object built on the threading.Thread class.
    Will set up a server and parse HTTP requests using HTTPRequestParser
    via the autocalled run() method when this Thread is start()ed. """

    ''' Update the server loop you built for the echo server so that it
    gathers an incoming request, parses it, and returns either a "200 OK"
    or an appropriate HTTP error. '''

    # The current implementation doesn't require threading on its own,
    # but it's easy to copy this class and replace the run() method
    # with the code needed for a client to ease testing.

    def __init__(self, ip_address='127.0.0.1', port_number=50000):

        super(ThreadedHTTPServer, self).__init__()

        self.ip_address = ip_address
        self.port_number = port_number

    def set_up_server(self):

            self.server_socket = socket.socket(socket.AF_INET,
                                               socket.SOCK_STREAM,
                                               socket.IPPROTO_TCP)

            self.server_socket.bind((self.ip_address, self.port_number))

            self.server_socket.listen(1)

            self.connection, self.client_address = self.server_socket.accept()

    def run(self):

        try:

            # Set up the server once, outside the while loop.
            self.set_up_server()

            while True:

                # Receive data continually.
                data = self.connection.recv(1024)

                if len(data) > 0:

                    # HTTPRequestParser is a custom-crafted instance
                    # of BaseHTTPRequestHandler that parses whatever
                    # HTTP request string is handed to it at call time.
                    # The parsed request can then have its parts referenced
                    # by checking self.parsed_http_response.partnamegoeshere
                    parsed_http_response = HTTPRequestParser(data)

                    # First, the catchall error case:
                    if parsed_http_response.error_code is not None:

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
                        self.connection.sendall("%s %s %s\r\n\r\n" % (
                            parsed_http_response.request_version,
                            parsed_http_response.error_code,
                            parsed_http_response.error_message))

                    # Second, the version forbidden case:
                    elif parsed_http_response.request_version != "HTTP/1.1":

                        ''' The function should only accept HTTP/1.1
                        requests, a request of any other protocol
                        should raise an appropriate error '''

                        print("[Sent] %s 505 HTTP Version Not Supported\r\n"
                              % (parsed_http_response.request_version))

                        self.connection.sendall(
                            "%s 505 HTTP Version Not Supported\r\n\r\n"
                            % (parsed_http_response.request_version))

                    # Third, the method forbidden case:
                    elif parsed_http_response.command != "GET":

                        ''' The function should only accept GET requests,
                        any other request should raise an appropriate error '''

                        print("[Sent] %s 405 Method Not Allowed\r\n"
                              % (parsed_http_response.command))

                        self.connection.sendall("%s 405 Method Not Allowed"
                                                "\r\n\r\n" %
                                                (parsed_http_response.command))

                    # Fourth, the acceptable request case:
                    elif parsed_http_response.error_code is None:

                        ''' Implement a function that will return
                        a well formed HTTP "200 OK" response as
                        a byte string suitable for transmission
                        through a socket. '''

                        # Apparently, "200 OK" is not an error code.
                        self.connection.sendall("%s 200 OK\r\n" %
                                                (parsed_http_response.
                                                 request_version))

                        print("[Sent] %s 200 OK" %
                              (parsed_http_response.request_version))

                        ''' Implement a function that will parse
                        an HTTP request and return the URI requested. '''

                        # After the request has been checked, return the URI.
                        self.connection.sendall(parsed_http_response.path + "\r\n\r\n")
                        #                        "\r\n\r\n")

                        print("[Sent] %s\r\n" % (parsed_http_response.path))

                # Breaking the server if client sends a blank line:
                if data == "\r\n" or data == "\r\n\r\n":

                    break

        finally:

            # Cleaning up the socket after we're done:
            if self.server_socket is not None:

                # debugging sanity check
                import time
                time.sleep(1)

                #self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()


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


def run_threads():

    server_thread = ThreadedHTTPServer()
    server_thread.start()
    server_thread.join()


if __name__ == "__main__":

    run_threads()
