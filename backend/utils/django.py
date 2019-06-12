import socket, sys
import socketserver, json, selectors
# import logging
import threading
import time
from slacker import Slacker
import os, json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = []

rssi = 0
buzzer_state = None
noteBookActivate = False
lock = False
fLock = False
rssiDist = 0

def slack_notify(text=None, channel='#backend', username='알림봇', attachments=None):
    TOKEN = "xoxb-623136227107-661697401447-782PfeMJFhmWMoTSwSaCkWzC"
    # TOKEN = get_secret("slackToken")
    slack = Slacker(TOKEN)
    attachments = [{
    "pretext": "경고 알림",
    # "color": "#36a64f",
    "color": "#ed2939",
    "title": "누군가가 노트북에 손을 댔습니다.",
    "title_link": "http://http://ec2-13-209-76-226.ap-northeast-2.compute.amazonaws.com:8080/img/",
    "fallback": "클라이언트에서 노티피케이션에 보이는 텍스트 입니다. attachment 블록에는 나타나지 않습니다",
    # "image_url": "http://127.0.0.1:8000/img/",
    "text": "자세히 보기 대충 이런 내용입니다.",
    "mrkdwn_in": ["text", "pretext"],
    }]
    # "text": "{}".format(book.title)

    slack.chat.post_message(text=text, channel=channel, username=username, attachments=attachments)


class note_book_server(socketserver.StreamRequestHandler):
    def handle(self):
        global noteBookActivate, fLock, lock, rssiDist
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
                print('Windows locked : True')
            else:
                print('Windows locked : False')

            if fLock:
                print('Logon failed : True')
            else:
                print('Logon failed : False')
            print(rssiDist)

            response = dict(status=status, deviceid=request.get('deviceid'),
                            msgid=request.get('msgid'))
            if rssiDist > 8:
                response['noteBookActivate'] = True
            else:
                response['noteBookActivate'] = False
            if response.get('noteBookActivate'):
                print(response.get('deviceid'), ' - Status - noteBookActivate : True')
            else:
                print(response.get('deviceid'), ' - Status - noteBookActivate : False')
            response = json.dumps(response)
            self.wfile.write(response.encode('utf-8') + b'\n')
            self.wfile.flush()


        print('Client closing: {}'.format(client))

class raspberry_post_server(socketserver.StreamRequestHandler):
    def handle(self):
        global buzzer_state, rssiDist, fLock

        client = self.request.getpeername()
        # logging.info("Client connecting: {}".format(client))

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
                # logging.error(error_msg)
                break
            else:
                status = 'OK'
                # logging.debug("{}:{}".format(client, request))


            # reply response message
            response = dict(status=status, deviceid=request.get('deviceid'),
                            msgid=request.get('msgid'))
            print('PI : ',rssiDist)
            print(type(rssiDist))
            if fLock:
                if (rssiDist > 8.1):
                    slack_notify()
                    print('Buzzer Activate')
                    response['activate'] = True
            else:
                response['activate'] = False

            if response.get('activate'):
                print(response.get('deviceid'), ' - Status - activate : True')
            else:
                print(response.get('deviceid'), ' - Status - activate : False')
            response = json.dumps(response)
            self.wfile.write(response.encode('utf-8') + b'\n')
            self.wfile.flush()

def raspberry_post():
    rasp_addr = ("", 8095)
    with socketserver.ThreadingTCPServer(rasp_addr, raspberry_post_server) as server:
        # logging.info('rasp Server starts: {}'.format(rasp_addr))
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
        # logging.info('rasp Server starts: {}'.format(notebook_addr))
        server.serve_forever()

e = threading.Thread(name='rasp', target=raspberry_post)
e.start()

server_for_notebook()

