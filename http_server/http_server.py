
import socket
import BaseHTTPServer
import StringIO
# for http response codes:
import datetime
# sdiehl.github.io/gevent-tutorial:
from gevent.server import StreamServer

# see: datetime httplib
# "size of the content" means number of bytes in the string
# opening on your file system with URLlib, using pathlib to get an absolute path (security violation)


# this function is still pseudocode!
def return_file_or_directory(path_from_httpparserclass):

    '''If the resource identified by the URI is a directory,
    return a simple HTML listing of that directory as the body.'''
    if uri == '/webroot' or '/webroot/':
        return listing of that directory

    elif uri == '/webroot/images' or '/webroot/images/':
        return listing of that directory

    else:

        # make this a top level function
        def figure_out_if_file_is_in_the_directory(filename_as_a_string):

            directory_list = # giant hardcoded directory list goes here for simplicity
            for each in directory_list:

                if uri == each:

                    ''' if the resource identified by the URI is a file,
                    return the contents of the file as the body.'''

                    # DO NOT do this in this function:
                    #headers = construct_a_header_with_content_type_in_it(uri_extension_string)
                    # INSTEAD do this in a separate function, craft_ok_http_response()


                    '''The content type value should be related to the type of file.'''


                    ''' Ensure that the body of the requested resource is returned in a "200 OK" response. '''
                    # to do this, make a second version of return_http_ok(parsed_http_response)
                    # that version will be the same as the first but with headers and content equal to the binary of the file (utf-8, python's string default, will be fine right?)

                    # DO NOT send it straight to
                    #socket_send_to_client(that_file.open(), headers)
                    # INSTEAD
                    return contents_of_the_file

                    # DO NOT do this in this function
                    #return ("<body>%s</body>" % (contents_of_the_file))
                    # INSTEAD do this in a separate function, craft_ok_http_response()

                ''' If the requested resource cannot be found,
                raise an appropriate error'''

                else:

                    ''' Any errors raised should be appropriately handled
                    and returned to the client as HTTP error responses
                    with appropriate codes. '''

                    return_file_not_found(parsed_http_response)




list of possible content types:

content_type = "text/html; charset=UTF-8"


def return_ok_http_file_response(parsed_http_response, file_data, content_type):
    ''' Craft a string response using data from
    the response parser, file data, and
    a content type string. '''

    ok_http_file_response = ("%s 200 OK\r\n"
                             "Date: %s\r\n"
                             "Content-Type: %s\r\n"
                             "\r\n"
                             "<!DOCTYPE HTML><html><body>%s</body></html>"
                             % (parsed_http_response.request_version,
                                datetime.datetime.now(),
                                content_type,
                                file_data))

return ok_http_file_response

def return_ok_http_directory_response(parsed_http_response, uri):
    ''' Craft a string response using data from
    the response parser, file data, and
    a content type string. '''

    ok_http_directory_response = ("%s 200 OK\r\n"
                                  "Date: %s\r\n"
                                  "Content-Type: %s\r\n"
                                  "\r\n"
                                  "<!DOCTYPE HTML><html><body>%s</body></html>"
                                  % (parsed_http_response.request_version,
                                     datetime.datetime.now(),
                                     content_type,
                                     file_data))

    return ok_http_file_response

def handle(socket, address):

    unparsed_data = socket.recv(1024)
    parsed_http_response = HTTPRequestParser(unparsed_data)

    # Message formatting and message sending are separated for ease of testing.

    if parsed_http_response.error_code is not None:
        server_response = return_error(parsed_http_response)
        socket.send(server_response)

    elif parsed_http_response.request_version != "HTTP/1.1":
        server_response = return_unsupported_version(parsed_http_response)
        socket.send(server_response)

    elif parsed_http_response.command != "GET":
        server_response = return_method_not_allowed(parsed_http_response)
        socket.send(server_response)

    elif parsed_http_response.error_code is None:
        server_response = return_http_ok(parsed_http_response)
        socket.send(server_response)

    socket.close()


#def send_message(socket, message):

#    socket.send(server_response)

# Zeroeth, the missing file case:
def return_file_not_found(parsed_http_response):
    ''' Any errors raised should be appropriately handled and returned
    to the client as HTTP error responses with appropriate codes. '''

    # This is effectively an internal error that requires me to define
    # what finding and not finding a file means before it can be triggered.
    return "%s 404 File not found ('%s')\r\n\r\n" & (
        parsed_http_response.request_version,
        parsed_http_response.path)


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
