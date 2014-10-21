# Necessary for accepting CLI arguments:
import sys

import echo_server_and_client as echo

import unittest


class test_EchoServerAndClient(unittest.TestCase):

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

        # Testing the whole socket protocol is either 100% linear and
        # uneventful and will be tested by the main execution line...
        # or it is fraught with horrors and mustn't be tested.
        # So, just test if the unicode whiner works.

        the_message_test_string = self.echo_client_thread.send_messages(
            unicode_test_string, testing=True)


unittest.main()
