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

    def reply(self, reply_code, response):
        self.send_response(reply_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response = "!".join(response)
        print("response:", response)

        # Send the html message
        self.wfile.write(bytes(response, "utf-8"))
        self.wfile.flush()

        return

    def process(self, request):
        response = []
        reply_code = 200

        print(request)

        if request[0] == "1" or request[0] == "2":
            # 1/2!username!password

            username = request[1]
            password = request[2]

            if(username in self.user2info and
                password == self.user2info[username]["password"]):
                hash_id = self.hash_function(username)
                self.hash2user[hash_id] = username
                response.append(hash_id)
            else:
                response.append("No")
                reply_code = 400

        elif request[0] == "3":
            # 3!hash_id!location

            hash_id = request[1]
            location = request[2]

            if hash_id not in self.hash2user:
                response.append("No")
            else:
                self.hash2loc[hash_id] = location
                self.pendreq2loc[hash_id] = location
                response.append("Yes")

        elif request[0] == "5":
            # 5!stu_hash_id!sec_hash_id!ETA

            student_hash_id = request[1]
            security_hash_id = request[2]
            eta = request[3]

            print("request %s, stu_id=%s, sec_id=%s" %
                  (5, student_hash_id, security_hash_id))

            if student_hash_id in self.pendreq2loc:
                del self.pendreq2loc[student_hash_id]
                self.stu2sec[student_hash_id] = [security_hash_id, False]
                student_username = self.hash2user[student_hash_id]
                student_info = self.user2info[student_username]
                student_location = self.hash2loc[student_hash_id]
                response.append(str(student_info))
                response.append(student_location)
            else:
                response.append("No")
                reply_code = 400
        
        elif request[0] == "6":
            # 6!stu_hash_id

            student_hash_id = request[1]
            self.stu2sec[student_hash_id][1] = True
            response.append("Yes")

        elif request[0] == "7":
            # 7!hash_id!location

            hash_id = request[1]
            location = request[2]
            username = self.hash2user[hash_id]
            self.hash2loc[hash_id] = location

            if self.user2info[username]["type"] == "student":
                # security: confirmed:
                if hash_id in self.stu2sec:
                    security_hash_id = self.stu2sec[hash_id]
                    security_username = self.hash2user[security_hash_id]
                    security_info = str(self.user2info[security_username])
                    security_location = str(self.hash2loc[security_hash_id])
                    response.append(security_info)
                    response.append("10")
                else:
                    reply_code = 400
                    response.append("No")

            elif self.user2info[username]["type"] == "security":
                # whether paired
                confirmed = False
                for student_hash_id in self.stu2sec:
                    security_hash_id = self.stu2sec[student_hash_id]
                    if security_hash_id == hash_id:
                        confirmed = True
                        response.append("Yes")

                if not confirmed:
                    for student_hash_id in self.pendreq2loc:
                        pickup_location = self.pendreq2loc[student_hash_id]
                        response.append(student_hash_id)
                        response.append(pickup_location)

        elif request[0] == "8":
            # 8
            for student_hash_id in self.pendreq2loc:
                pickup_location = self.pendreq2loc[student_hash_id]
                response.append(student_hash_id)
                response.append(pickup_location)
        else:
            response.append("No")
            reply_code = 400

        return response, reply_code

    def hash_function(self, username):
        # return hashlib.md5(username).hexdigest()
        return username

    # Handler requests
    def do_GET(self):
        print('Get request received')
        print('request:', self.path)

        print("hash2user:", self.hash2user)
        print("user2info:", self.user2info)
        print("hash2loc:", self.hash2loc)
        print("pendreq2loc:", self.pendreq2loc)
        print("stu2sec:", self.stu2sec)
        print("\n")

        request = self.parse(self.path[1:])
        response, reply_code = self.process(request)
        self.reply(reply_code, response)
        return

server = pennappserver()
server.start()
