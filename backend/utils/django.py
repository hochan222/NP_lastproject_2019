import socket, sys
import socketserver, json, selectors
import logging
import threading
import time
from slacker import Slacker
import os, json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

rssi = 0
buzzer_state = None
noteBookActivate = False
lock = False
fLock = False
rssiDist = 0

class note_book_server(socketserver.StreamRequestHandler):
    def handle(self):
        global noteBookActivate, flock, lock, rssiDist
        client = self.request.getpeername()
        print("Client connecting: {}".format(client))

        for line in self.rfile:
            try:
                request = json.loads(line.decode('utf-8'))
            except ValueError as e:
                error_msg = '{}: json decoding error'.format(e)
                status = 'ERROR {}'.format(error_msg)
                response = dict(status=status, deviceid=request.get('deviceid'),
                                msgid=request.get('msgid'))
                response = json.dumps(response)
                self.wfile.write(response.encode('utf-8') + b'\n')
                self.wfile.flush()
                print(error_msg)
                break
            else:
                status = 'OK'
                print("{}:{}".format(client, request))

            data = request.get('data')
            if data:
                lock = data.get('lock')
                fLock = data.get('fLock')
                frame = data.get('image')

            with open(os.path.join(BASE_DIR, 'data_file.json'), "w") as write_file:
                json.dump(data, write_file)
            with open(os.path.join(BASE_DIR, 'rssi_data.json')) as outfile:
                rssiData = json.load(outfile)

            rssiDist = rssiData['dist']

            if lock:
                print('Windows is locked!')

            if fLock:
                print('Logon failed ditected!')
                try:
                    pass
                    #cv2.imwrite('image.png',frame)
                except Exception as e:
                    print('Image not saved!')

            response = dict(status=status, deviceid=request.get('deviceid'),
                            msgid=request.get('msgid'))
            if rssiDist > 8:
                response['noteBookActivate'] = True
            else:
                response['noteBookActivate'] = False
            response = json.dumps(response)
            self.wfile.write(response.encode('utf-8') + b'\n')
            self.wfile.flush()
            if response.get('noteBookActivate'):
                print(response.get('deviceid'), ' - Status - noteBookActivate : True')
            else:
                print(response.get('deviceid'), ' - Status - noteBookActivate : False')

        print('Client closing: {}'.format(client))

class raspberry_post_server(socketserver.StreamRequestHandler):
    def handle(self):
        global buzzer_state, rssiDist, flock

        client = self.request.getpeername()
        logging.info("Client connecting: {}".format(client))

        for line in self.rfile:
            try:
                request = json.loads(line.decode('utf-8'))
            except ValueError as e:
                # reply ERROR response message
                error_msg = '{}: json decoding error'.format(e)
                status = 'ERROR {}'.format(error_msg)
                response = dict(status=status, deviceid=request.get('deviceid'),
                                msgid=request.get('msgid'))
                response = json.dumps(response)
                self.wfile.write(response.encode('utf-8') + b'\n')
                self.wfile.flush()
                logging.error(error_msg)
                break
            else:
                status = 'OK'
                logging.debug("{}:{}".format(client, request))


            # reply response message
            response = dict(status=status, deviceid=request.get('deviceid'),
                            msgid=request.get('msgid'))

            if (rssiDist < 8 or fLock):
                #slack_notify()
                response['activate'] = True
            else:
                response['activate'] = False


            response = json.dumps(response)
            self.wfile.write(response.encode('utf-8') + b'\n')
            self.wfile.flush()
            if response.get("activate"):
                print(response.get('deviceid'), ' - Status - activate : True')
            else:
                print(response.get('deviceid'), ' - Status - activate : False')

def raspberry_post():
    rasp_addr = ("", 8095)
    with socketserver.ThreadingTCPServer(rasp_addr, raspberry_post_server) as server:
        logging.info('rasp Server starts: {}'.format(rasp_addr))
        server.serve_forever()

def server_for_notebook():
    notebook_addr = ("", 5555)
    data = {
            'lock': False,
            'fLock': False,
            'image': 0
        }
    with open(os.path.join(BASE_DIR, 'data_file.json'), 'w') as outfile:
        json.dump(data, outfile)
    print('Server Done This is thread~')

    with socketserver.ThreadingTCPServer(notebook_addr, note_book_server) as server:
        logging.info('rasp Server starts: {}'.format(notebook_addr))
        server.serve_forever()

e = threading.Thread(name='rasp', target=raspberry_post)
e.start()

server_for_notebook()

