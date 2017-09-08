from http.server import BaseHTTPRequestHandler, HTTPServer
import time

PORT_NUMBER = 50008

# This class will handle any incoming request from
# a browser 

class pennappserver():

    # init maps 
    def __init__(self): 
        self.user2pw = {}
        self.hash2user = {}
        self.hash2info = {}
        self.hash2loc = {}
        self.pendreq2loc = {}
        self.esc2stu = {}

    def start(self):

        try:
            # Create a web server and define the handler to manage the
            # incoming request
            server = HTTPServer(('', PORT_NUMBER), myHandler)
            print ('Started httpserver on port ' , PORT_NUMBER)

            # Wait forever for incoming http requests
            server.serve_forever()

        except KeyboardInterrupt:
            print ('^C received, shutting down the web server')
            server.socket.close()

class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        print('Get request received')
        print('request:' + self.path)

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(bytes("Hello World !", "utf-8"))
        return

server = pennappserver()
server.start()





