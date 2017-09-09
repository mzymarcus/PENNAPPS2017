from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import hashlib

PORT_NUMBER = 50008

# This class will handle any incoming request from
# a browser 

class pennappserver():
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


    # init maps
    def __init__(self):
        self.user2pw = {}
        self.hash2user = {}
        self.hash2info = {}
        self.hash2loc = {}
        self.pendreq2loc = {}
        self.stu2sec = {}

    def parse(self, raw_request):
        return raw_request.split("`")

    def reply(self, response):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        "`".join(response)
        # Send the html message
        self.wfile.write(bytes(response, "utf-8"))

    def process(self, request):
        response = []
        if request[0] == 1:
            # 1`username`password
            self.user2pw[request[1]] = request[2]
            print_map(self.user2pw, "user2pw")
            

        elif request[0] == 2:
            # 2`username`password
            self.user2pw[request[1]] = request[2]
            print_map(self.user2pw, "user2pw")

        elif request[0] == 3: 
            # 3`hash`location
            hash_id = request[1]
            location = request[2]

        elif request[0] == 5:
            student_hash_id = request[1]
            security_hash_id = request[2]
            if student_hash_id in self.pendreq2loc:
                del self.pendreq2loc[student_hash_id]
                self.stu2sec[student_hash_id] = security_hash_id

                response.append("Yes")
            else:
                response.append("No")
        elif request[0] == 6:
            pass
        elif request[0] == 7:
            pass
        elif request[0] == 8:
            pass

        return response

    def print_map(dict_map, map_name):
        print(map_name + ":")
        for key in dict_map:
            print(key + ',' + dict_map[key])

    # Handler requests
    def do_GET(self):
        print('Get request received')
        print('request:' + self.path)

        request = self.parse(self.path)
        self.reply(response)
        return

server = pennappserver()
server.start()





