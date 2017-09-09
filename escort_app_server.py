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

    user2pw = {"gavin": "123", "dalige": "123", "mage": "123", "wuwang": "123"}

    hash2user = {}

    # info {username, password, type, picture ...}
    user2info = {"gavin": {"password": "123", "type": "student",},
                 "dalige": {"password": "123", "type": "security",},
                 }
    hash2loc = {}
    pendreq2loc = {}
    stu2sec = {}

    def parse(self, raw_request):
        return raw_request.split("!")

    def reply(self, response):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response = "!".join(response)
        print("response:" + response)

        # Send the html message
        self.wfile.write(bytes(response, "utf-8"))

    def process(self, request):
        response = []

        print(request)

        if request[0] == "1" or request[0] == "2":
            # 1 username password

            username = request[1]
            password = request[2]

            if(username in self.user2info and
                password == self.user2info[username]["password"]):
                hash_id = self.hash_function(username)
                self.hash2user[hash_id] = username
                response.append(hash_id)
            else:
                response.append("No")

        elif request[0] == "3":
            # 3 hash_id location

            hash_id = request[1]
            location = request[2]

            self.hash2loc[hash_id] = location
            self.pendreq2loc[hash_id] = location

            self.print_map(self.hash2loc, "hash2loc")
            self.print_map(self.pendreq2loc, "pendreq2loc")

            response.append("received")

        elif request[0] == "5":
            # 5 stu_hash_id sec_hash_id

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
            # 7!hash_id!location
            hash_id = request[1]
            username = self.hash2user[hash_id]
            location = request[2]

            if
            # STUDENT: INIT, REPLY YES
            # STUDENT: WAITING, REPLY SECURITY PROFILE
            # STUDENT: CONFIRMED, REPLY SECURITY LOCATION

            # SECURITY: INIT, REPLY PENDING REQUEST
            # SECURITY: CONFIRMED, REPLY YES



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

        request = self.parse(self.path[1:])
        response = self.process(request)
        self.reply(response)
        return

server = pennappserver()
server.start()
