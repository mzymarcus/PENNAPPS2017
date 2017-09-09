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

    user2pw = {}
    hash2user = {}
    hash2info = {}
    hash2loc = {}
    pendreq2loc = {}
    stu2sec = {}

    def parse(self, raw_request):
        return raw_request.split("`")

    def reply(self, response):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response = "`".join(response)

        # Send the html message
        self.wfile.write(bytes(response, "utf-8"))

    def process(self, request):
        response = []

        if request[0] == "1":
            # 1`username`password

            username = request[1]
            password = request[2]
            hash_id = self.hash_function(username)

            self.user2pw[username] = password
            self.hash2user[hash_id] = username

            self.print_map(self.user2pw, "user2pw")
            self.print_map(self.hash2user, "hash2user")

            response.append(hash_id)

        elif request[0] == "2":
            # 2`username`password

            username = request[1]
            password = request[2]
            hash_id = self.hash_function(username)

            self.user2pw[username] = password
            self.hash2user[hash_id] = username

            self.print_map(self.user2pw, "user2pw")
            self.print_map(self.hash2user, "hash2user")

            response.append(hash_id)

        elif request[0] == "3":
            # 3`hash_id`location

            hash_id = request[1]
            location = request[2]

            self.hash2loc[hash_id] = location
            self.pendreq2loc[hash_id] = location

            self.print_map(hash2loc, "hash2loc")
            self.print_map(pendreq2loc, "pendreq2loc")

            response.append("YES")

        elif request[0] == "5":
            student_hash_id = request[1]
            security_hash_id = request[2]
            print("request %s, stu_id=%s, sec_id=%s" %
                  (5, student_hash_id, security_hash_id))
            if student_hash_id in self.pendreq2loc:
                del self.pendreq2loc[student_hash_id]
                self.stu2sec[student_hash_id] = [security_hash_id, False]
                response.append("Yes")
            else:
                response.append("No")
        
        elif request[0] == "6":
            student_hash_id = request[1]
            self.stu2sec[student_hash_id][1] = True

        elif request[0] == "7":
            # 7`hash_id`location
            hash_id = request[1]
            location = request[2]

            hash2loc[hash_id] = location
            self.print_map(self.hash2loc, "hash2loc")
            response.append("YES")

        elif request[0] == "8":
            for student_hash_id in self.pendreq2loc:
                pickup_location = self.pendreq2loc[student_hash_id]
                response.append(student_hash_id)
                response.append(pickup_location)
        else:
            pass

        return response

    def hash_function(self, username):
        # return hashlib.md5(username).hexdigest()
        return username

    def print_map(self, dict_map, map_name):
        print(map_name + ":")
        for key in dict_map:
            print(key + ',' + dict_map[key])

    # Handler requests
    def do_GET(self):
        print('Get request received')
        print('request: ' + self.path)

        request = self.parse(self.path)
        response = self.process(request)
        self.reply(response)
        return

server = pennappserver()
server.start()
