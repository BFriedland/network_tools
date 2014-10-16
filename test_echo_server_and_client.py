import socket
import time
import threading
# Necessary for accepting CLI arguments:
import sys

import echo_server_and_client as echo

import unittest


class test_EchoServerAndClient(unittest.TestCase):

    '''
    def setUp(self):

        # This tests the ServerThread constructor.
        self.echo_server_thread = echo.ServerThread()

        # This tests the ClientThread constructor.
        self.echo_client_thread = echo.ClientThread()

        echo.run_threads()
    '''
    '''
    def tearDown(self):

        self.echo_client_thread.join()
        self.echo_server_thread.join()

        #self.echo_client_thread.client_socket.shutdown(SHUT_WR)
        self.echo_client_thread.client_socket.close()

        #self.echo_server_thread.server_socket.shutdown(SHUT_WR)
        self.echo_server_thread.server_socket.close()
    '''

    def test_set_up_client(self):

        self.echo_client_thread = echo.ClientThread()
        self.echo_server_thread = echo.ServerThread()

        # Calling this function also tests echo.run_threads() and the
        # __init__(), set_up_server and run() commands of both threads.

    def test_enlistify_cli_arguments(self):

        self.test_set_up_client()

        # Manually modify sys.argv to change the result of calling this method:
        del sys.argv[1:]
        sys.argv.append('This is a test')
        sys.argv.append("This is also a test")
        sys.argv.append(5599)

        resulting_list = self.echo_client_thread.enlistify_cli_arguments()

        # The first argument is necessarily the program name.
        # It is not to be tested.
        # I don't want a segfault or something.
        # (( Note that the first thing in sys.argv[] is already skipped
        # by enlistify_cli_arguments() ))
        self.assertEqual(resulting_list[0], 'This is a test')
        self.assertEqual(resulting_list[1], "This is also a test")
        self.assertEqual(resulting_list[2], 5599)

        # self.tearDown()

    def test_send_messages(self):

        self.test_set_up_client()

        unicode_test_string = u'This is a unicode test string.'

        # Manually modify sys.argv to insert
        # a unicode string into the CLI args:
        del sys.argv[1:]
        sys.argv.append(u'This is a unicode test string.')

        # self.test_echo_server_and_client_together()

        # Testing the whole socket protocol is either 100% linear and
        # uneventful and will be tested by the main execution line...
        # or it is fraught with horrors and mustn't be tested.
        # So, just test if the unicode whiner works.

        the_message_test_string = self.echo_client_thread.send_messages(
            unicode_test_string, testing=True)

        # ...

        # The testing framework has decided they don't want
        # test-created threads to have sockets without running
        # the full server program, for some reason.
        # Got to test it with test_echo_server_and_client() instead.


unittest.main()
