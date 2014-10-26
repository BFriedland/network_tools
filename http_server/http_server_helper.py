
# Because, for some sadistic reason, I must master sockets:
import socket
# For easy parsing of the HTTP requests:
import BaseHTTPServer
# Helps BaseHTTPServer:
import StringIO
# For making http response headers:
import datetime
# sdiehl.github.io/gevent-tutorial:
from gevent.server import StreamServer
# So we can manage the directory:
import os

import gevent_server

# see: datetime httplib
# "size of the content" means number of bytes in the string
# opening on your file system with URLlib, using pathlib to get
# an absolute path (security violation)


def return_listing_of_this_directory(supplied_directory_path):

    # Chop the webroot off before searching for a directory.
    # I'm including this secondary assurance that /webroot/ is the path
    # being requested by the user because it would be insecure to allow
    # a user to access the base server files, and it's conceivable
    # the next person to maintain this code base will put in some function
    # which wouldn't check for webroot-specificity.
    # The constant 9 is simply /webroot/
    # This assumes all paths in HTTPRequestParser.path are always
    # going to be something like /webroot/images/testimage.jpg
    # That is, all calls to the server looking for a file or folder
    # will start this way.
    supplied_directory_path = supplied_directory_path[9:]
    supplied_directory_path = "./webroot/" + supplied_directory_path
    # ...
    # This works, but I didn't really need to remove /webroot/ and replace it
    # if I'm going to add "." at the front, since you can't get any kind of
    # insecurities while being entirely contained within /webroot/.
    # Leaving it in because I'm still behind on assignments and
    # these comments should make it clear how to change it to be
    # less application-specific.

    # List comprehension.
    return [each_thing for each_thing in
            os.listdir(supplied_directory_path)]


def return_requested_file_or_directory(parsed_http_response):

    '''If the resource identified by the URI is a directory,
    return a simple HTML listing of that directory as the body.

    Return a string containing HTML-formatted directory info
    or whatever data is in the file requested. '''

    # Initialize the content type to reflect the fact that
    # non-file content is going to have to be text/html:
    content_type = 'text/html; charset=UTF-8'

    internal_error = None

    # I know there's some more procedural way to generate these directory
    # listings, but it could take me longer to figure out how to make it
    # than to hardcode our only two cases.
    # Plus there might be more security issues to consider.

    # Don't accept '/webroot' or '/webroot/images' if
    # they don't have a trailing forward slash.
    if parsed_http_response.path == '/webroot/':

        list_of_this_directory = \
            return_listing_of_this_directory(parsed_http_response.path)

        # Crafting html here, since the specifications say to return
        # a directory listing in this part of the conditional
        # rather than a file.
        return_string = "<pre>/webroot</pre>"

        # For some reason I can't insert  tags here.
        # Only \n will display properly, since SOMETHING is
        # putting <pre></pre> tags around all of my content!
        # I have no idea what or why and the internet didn't know either.
        # ...
        # I was returning it from the wrong function.
        # It was calling return_requested_file_or_directory() instead,
        # which did not provide a header that would tell the browser
        # what the content type was.
        # I fixed this by pointing it to the correct function,
        # return_ok_http_file_or_directory_response().
        # ...
        # There must be a special tag for indenting things.
        # HTML ignored my indenting spaces untill I <pre></pre> formatted them.
        # Also this made the break tags superfluous since
        # the pre tags add breaks anyways.
        for each_file_or_folder in list_of_this_directory:
            return_string += \
                "<pre>    " + str(each_file_or_folder) + "</pre>"

    elif parsed_http_response.path == '/webroot/images/':

        list_of_this_directory = \
            return_listing_of_this_directory(parsed_http_response.path)

        # Crafting html here, since the specifications say to return
        # a directory listing in this part of the conditional
        # rather than a file.
        return_string = "<pre>/webroot</pre><pre>    /images</pre>"

        for each_file_or_folder in list_of_this_directory:
            return_string += \
                "<pre>        " + str(each_file_or_folder) + "</pre>"

    else:

        try:

            # This lets us chop off the start of the string
            # and replace it with "./webroot/"
            file_path = parsed_http_response.path
            file_path = file_path[9:]
            file_path = "./webroot/" + file_path

            # Takes newlines out of the file:
            with open(file_path, "r") as the_requested_file:
                file_data = the_requested_file.read().replace('\n', '')
                file_data = ''.join(file_data)

                # other possibility:
                # file_data = the_requested_file.read()

                return_string = file_data

            # Check if the file has a three-character extension:
            if file_path[-4:][0] == ".":
                # If it does, set the content_type equal to the extension.
                content_type = file_path[-4:]

        # Yes, this is where the 404 goes.
        # Remember, it's the trailing else: part of this conditional,
        # so it will grab all the possible misspellings etc.
        except:

            # Then the request is not in the directory.
            #return_string = \
            #    return_file_not_found(parsed_http_response)
            return_string = "file_not_found"

    return return_string, content_type


def return_ok_http_file_or_directory_response(parsed_http_response):

    # NOTE! This function returns two different pieces of information.
    # The specifications require content type in addition to file data
    # or directory listing.

    data_string, content_type_string = \
        return_requested_file_or_directory(parsed_http_response)

    if data_string == "file_not_found":

        formatted_response = return_file_not_found(parsed_http_response)

    else:

        formatted_response = ("%s 200 OK\r\n"
                              "Date: %s\r\n"
                              "Content-Type: %s\r\n"
                              "\r\n"
                              "<!DOCTYPE HTML><html><body>%s</body></html>"
                              "\r\n\r\n"
                              % (parsed_http_response.request_version,
                                 datetime.datetime.now(),
                                 content_type_string,
                                 data_string))

    return formatted_response


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
        # note to self: feed the returns from
        # return_requested_file_or_directory()
        # into a response crafter which does header creation.
        server_response = \
            return_ok_http_file_or_directory_response(parsed_http_response)
        socket.send(server_response)

    socket.close()


# Zeroeth, the missing file case:
def return_file_not_found(parsed_http_response):
    ''' Any errors raised should be appropriately handled and returned
    to the client as HTTP error responses with appropriate codes. '''

    # This is effectively an internal error that requires me to define
    # what finding and not finding a file means before it can be triggered.
    return "%s 404 File not found ('%s')\r\n\r\n" % (
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
    http_server = StreamServer(('127.0.0.1', 50000), gevent_server.handle)
    http_server.serve_forever()


if __name__ == "__main__":

    run_server()
