import socket

import threading

# For parsing HTTP requests.
# Courtesy of the solution AT:
# http://stackoverflow.com/questions/4685217/parse-raw-http-headers
# The BaseHTTPRequestHandler can parse HTTP requests and figure out which
# error applies for a given request automatically.
from BaseHTTPServer import BaseHTTPRequestHandler
# Also from the above-linked SO solution, this library will interpret strings
# as files. This simplifies the process of separating lines
# when parsing HTTP requests.
from StringIO import StringIO


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

            self.data = self.server_side_connection.recv(1024)

            self.parsed_http_request = HTTPRequestParser(self.data)

            print self.parsed_http_request.error_code       # None  (check this first)
            print self.parsed_http_request.command          # "GET"
            print self.parsed_http_request.path             # "/who/ken/trust.html"
            print self.parsed_http_request.request_version  # "HTTP/1.1"
            print len(self.parsed_http_request.headers)     # 3
            print self.parsed_http_request.headers.keys()   # ['accept-charset', 'host', 'accept']

        finally:

            # Always close the socket before leaving.
            self.server_socket.close()

    '''
    def return_http_response(self, which_http_code):

        """ Returns whichever kind of HTTP response
        is requested as the first parameter. """

        http_error_dictionary = {

            "ok": bytearray('HTTP/1.0 200 OK'),
            "moved": bytearray('HTTP/1.0 301 Moved Permanently'),
            "wrong_credentials": bytearray('HTTP/1.0 401 Wrong Credentials'),
            "forbidden": bytearray('HTTP/1.0 403 Forbidden'),
            "not_found": bytearray('HTTP/1.0 404 Not Found'),
            "internal_error": bytearray('HTTP/1.0 500 Internal Server Error'),

        }

        try:

            return 'HTTP/1.0' + http_error_dictionary[which_error_type] \
                + '\r\n\r\n'

        except:

            raise Exception
    '''

    """
    # def parse_http_request(self, the_request_to_parse):

        # example of non-operator string joins
        request_text = (
            'GET /who/ken/trust.html HTTP/1.1\r\n'
            'Host: cm.bell-labs.com\r\n'
            'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3\r\n'
            'Accept: text/html;q=0.9,text/plain\r\n'
            '\r\n'
        )
    """


class HTTPRequestParser(BaseHTTPRequestHandler):

    """ Return an object that contains variables for  of
    the http_request it is provided as a parameter. """

    def __init__(self, http_request):

        # Every variable and method name in this class is directly from
        # BaseHTTPRequestHandler itself.
        # They are being set and called in the poorly-interfaced manner
        # BaseHTTPRequestHandler requires.

        self.rfile = StringIO(http_request)
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
    server_thread = ServerThread()
    server_thread.start()

    server_thread.join()


if __name__ == "__main__":

    run_threads()














































































