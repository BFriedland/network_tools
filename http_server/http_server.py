import socket

import threading


class ThreadedHTTPServer(threading.Thread):

    def __init__(self, ip_address, port_number):

        super(ThreadedHTTPServer, self).__init__()

        self.ip_address = ip_address

        self.port = port_number

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP)


    def run():

        try:

            self.server_socket.bind(self.ip_address)
            self.server_socket.listen(1)

        finally:
            self.server_socket.close()



    def return_http_ok():

        return bytearray('HTTP/1.0 200 OK')

    def return_http_error(which_http_code):

        http_error_dictionary = {

            "ok": bytearray('HTTP/1.0 200 OK'),
            "moved": bytearray('HTTP/1.0 301 Moved Permanently'),
            "wrong_credentials": bytearray('HTTP/1.0 401 Wrong Credentials'),
            "forbidden": bytearray('HTTP/1.0 403 Forbidden'),
            "not_found": bytearray('HTTP/1.0 404 Not Found'),
            "internal_error": bytearray('HTTP/1.0 500 Internal Server Error'),

        }

        try:

            return http_error_dictionary[which_error_type]

        except:

            raise

































































































