import unittest
import http_server as http
import threading
import socket


# This test module is intended to be run
# while the server is running separately.


class test_ThreadedHTTPServer(unittest.TestCase):

    # Assume it's already set up to save time
    # def setUp(self):

    #    self.http_server_thread = http.ThreadedHTTPServer()

    #    self.http_server_thread.run()

    def test_all_http_responses(self):

        # This function runs all the tests for HTTP
        # responses without closing the server.
        # I did this because opening and closing the server involves
        # unpredictable socket timing that seems to have problems
        # separate from my threading. It's as if the socket has a delay before
        # it unassigns the address, even after close() has been called on it.

        # I'm not really sure how to design unit tests for this socket-level
        # program without spending even more days reading up on it
        # and trying to figure out how to make the socket free up faster than
        # close() appears to be working.

        list_of_test_strings = ["GET / HTTP/1.1\r\n", "GET / HTTP/1.0\r\n"]

        test_server = http.ThreadedHTTPServer()

        print("Test Server Initted")

        test_server.run()
        print("Test Server Run")

        test_client = ThreadedHTTPClient(list_of_test_strings)
        print("Test Client Initted")

        list_of_test_results = test_client.run()
        print("Test Client Run")

        self.assertEqual(list_of_test_results[0][:15], "HTTP/1.1 200 OK")

        self.assertEqual(list_of_test_results[1][:39],
                         "HTTP/1.0 505 HTTP Version Not Supported")





        test_200_ok()

        test_505()



        # After all tests are run, issue a shutdown command to the server:
        self.client_socket = ThreadedHTTPClient("\r\n\r\n")

        self.client_socket.run()

# The ThreadedHTTPClient is only needed for testing the server.
# Because it isn't in the specs and is used exclusively for testing,
# I put it in the testing file.


class ThreadedHTTPClient(threading.Thread):

    """ Return an HTTP client object built on the threading.Thread class.
    Will set up a client and issue HTTP requests via the autocalled run()
    method when this Thread is start()ed. """

    def __init__(self, list_of_test_strings, ip_address='127.0.0.1',
                 port_number=50000):

        super(ThreadedHTTPClient, self).__init__()

        self.ip_address = ip_address
        self.port_number = port_number
        self.list_of_test_strings = list_of_test_strings

    def set_up_client(self):

            self.client_socket = socket.socket(socket.AF_INET,
                                               socket.SOCK_STREAM,
                                               socket.IPPROTO_TCP)

            self.client_socket.connect((self.ip_address, self.port_number))



    def run(self):








        # It's not even attempting to try: and skipping straight to finally:,
        # I don't know why, and I'm out of time.

        # Assume the server is already set up to save time
        #self.setUp()

        self.set_up_client()

        for each_test_string in self.list_of_test_strings:

            print("Got into the try block in run()")

            # First, issue the request to the server to test its response:
            self.client_socket.sendall(each_test_string)

            print("Got past sendall, sending %s" % (each_test_string))

            # Receive the server's response and store it to return
            # after the socket is closed:
            data_to_return = self.client_socket.recv(1024)

            if data_to_return is None:
                print("uhoh, data_to_return is NONE")
            print(data_to_return)

            self.list_of_return_strings.append(data_to_return)





        self.client_socket.sendall("\r\n\r\n")


        self.client_socket.close()


        return self.list_of_return_strings


        '''
        try:

            self.set_up_client()

            print("Got into the try block in run()")

            # First, issue the request to the server to test its response:
            self.client_socket.sendall(self.string_to_test)

            print("Got past sendall")

            # Receive the server's response and store it to return
            # after the socket is closed:
            self.data_to_return = client_socket.recv(1024)

            if self.data_to_return is None:
                print("uhoh, data_to_return is NONE")
            print(self.data_to_return)

            #self.client_socket.sendall("\r\n\r\n")

            self.client_socket.close()


        except:

            print("Hit the finally block")

            # Cleaning up the socket after we're done:
            if self.client_socket is not None:

                #self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()

            return self.data_to_return
        '''

unittest.main()
