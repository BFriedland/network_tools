import http_server
import unittest


class ThreadedClientForTesting(threading.Thread):

    def __init__(self):

        super(ThreadedClientForTesting, self).__init__()

    def set_up_client(self):

            self.client_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_IP)

            self.address_for_this_process = ('127.0.0.1', 50000)

            self.client_socket.connect(self.address_for_this_process)

    def run(self, testing_message):

        ''' When this thread is called, send just one
        presanitized test message for testing HTTPServer. '''

        try:

            self.set_up_client()

            self.client_socket.sendall(testing_message)

            self.client_socket.shutdown(socket.SHUT_WR)

        finally:

            self.client_socket.close()




class test_HTTPServer(unittest.TestCase):


    def test_set_up_server(self):

        ''' Test set_up_server. Initializes the environment  '''

        self.http_server_thread = http_server.HTTPServerThread
        self.http_server_thread.set_up_server()


    def test_run_threads(self):

        self.test_client_thread = ThreadedClientForTesting()
        run_threads()










