network_tools
=============


gevent_server.py

    An HTTP server program running via gevent that provides access to
        files in a directory.

    When called with /webroot/ or /webroot/images as the URI, it will
        return an HTML-formatted directory listing.
    When called with the path of a file in the directory, it will
        return the contents of that file as a binary.

    Dependencies include gevent and Python 2.7, plus my internal files
        http_server_helper and the webroot directory.

    There are two global functions and one class.

        handle(), which runs the server's request-response cycle.

        HTTPRequestParser(BaseHTTPServe.BaseHTTPRequestHandler), takes
            an HTTP request and returns an object containing that request,
            parsed in attributes.

            send_error() overwrites BaseHTTPServer.BaseHTTPRequestHandler's
                previous send_error method.

        run_server(), starts gevent's StreamServer, set to handle untill
            the server is manually closed with an interrupt command.
            This function is called when the file is run.

    References/helped by reading/partial copies/paraphrasing:

        http://stackoverflow.com/questions/4685217/parse-raw-http-headers

        sdiehl.github.io/gevent-tutorial

        http://stackoverflow.com/questions/8369219/
            how-do-i-read-a-text-file-into-a-string-variable-in-python


echo_server_and_client.py

    A very simple socket communications example program.

    You run it, it takes whatever text-based command line arguments you
        provide, and it will send them through a socket and print them as text.

    Dependencies include only Python 2.7

    There are three internal calls, but they don't need to be accessed
        and are only intended to interact with the rest of this program:

        ClientThread() returns a ClientThread object inheriting from
            threading.Thread with:

            set_up_client() method that will initialize itself to:

                self.socket_client, a socket.socket() with settings
                    AF_INET, SOCK_STREAM and IPPROTO_IP

                self.address_for_this_process, which defaults to a tuple
                    containing (localhost, 50000) ((as IP and port number))

                call connect(self.address_for_this_process) on the
                    socket_client

            enlistify_cli_arguments() method that will take all of the
                command line arguments except the name of the program
                and return them as a list

            send_messages(messages) method that will take any list of
                ASCII strings supplied to it and attempt to turn them
                into bytecode, which it then attempts to send through
                the socket

            run() method that is called by the run_threads function at
                the module level. It will set up the client and attempt
                to send the CLI arguments provided to the program through
                the socket. It should close the socket properly when completed.

        ServerThread() returns a ServerThread object inheriting from
            threading.Thread with:

            set_up_server() method that will initialize itself to:

                self.server_socket, a socket.socket() with settings
                    AF_INET, SOCK_STREAM and IPPROTO_IP

                self.address_for_this_process, which defaults to a tuple
                    containing (localhost, 50000) ((as IP and port number))

                call bind(self.address_for_this_process) on the server_socket

                call listen(1) on the server_socket

                assign the result of calling accept() on the server_socket
                    to the class attributes server_side_connection and
                    server_side_client_address

            run() method that is called by the run_threads function at
                the module level. It will call set_up_server and assign the
                results of calling recv(32) on the server_side_connection
                to the class attribute named data and then call print on
                the class attribute named data. It should close the socket
                properly when completed.

        run_threads() creates a ServerThread and starts it, creates
            a ClientThread and starts it, and then calls join() on both the
            server thread and the client thread separately.

    References/helped by reading/partial copies/paraphrasing:

        http://stackoverflow.com/questions/196345/how-to-check-if-a-string-
            in-python-is-in-ascii

        http://www.diveintopython.net/scripts_and_streams/command_line_
            arguments.html

        https://github.com/zappala/python-networking-and-threading/blob/
            master/echo-server/echoserver.py

        http://stackoverflow.com/questions/576169/understanding-python-
            super-and-init-methods

        http://stackoverflow.com/questions/2846653/python-multithreading-
            for-dummies

        http://www.experts-exchange.com/Programming/System/Q_28378122.html

        http://stackoverflow.com/questions/1274047/why-isnt-assertraises-
            catching-my-attribute-error-using-python-unittest
