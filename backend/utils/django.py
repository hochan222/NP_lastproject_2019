import socket, sys
import socketserver, json, selectors
import logging
import threading
import time

from slacker import Slacker
import os, json


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = []
# secret_file = os.path.join(BASE_DIR, 'secret', 'slack_token.json')

# with open(secret_file) as f:
#     secrets = json.loads(f.read())

# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets["slackToken"]
#     except KeyError:
#         error_msg = "Set the {} environment variable".format(setting)
#         raise ImproperlyConfigured(error_msg)

def slack_notify(text=None, channel='#backend', username='알림봇', attachments=None):
    # TOKEN = get_secret("slackToken")
    TOKEN = "xoxb-623136227107-661697401447-ct3yujlEtdFnRCLwK8jP2Lcz"
    slack = Slacker(TOKEN)
    attachments = [{
    "pretext": "경고 알림",
    # "color": "#36a64f",
    "color": "#ed2939",
    "title": "누군가가 노트북에 손을 댔습니다.",
    "title_link": "http://127.0.0.1:8000/img/",
    "fallback": "클라이언트에서 노티피케이션에 보이는 텍스트 입니다. attachment 블록에는 나타나지 않습니다",
    # "image_url": "http://127.0.0.1:8000/img/",
    "text": "자세히 보기 대충 이런 내용입니다.",
    "mrkdwn_in": ["text", "pretext"],
    }]
    # "text": "{}".format(book.title)

    slack.chat.post_message(text=text, channel=channel, username=username, attachments=attachments)


# main: 10007, rssi_renew_thread: 8090
# raspberry: 8095

rssi = 0
buzzer_state = None
# django main server
class IoTRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        global rssi
        global buzzer_state

        client = self.request.getpeername()
        logging.info("Client connecting: {}".format(client))

        for line in self.rfile:
            # get a request message in JSON and converts into dict
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

            # extract the sensor data from the request
            data = request.get('data')
            if data:        # data exists
                rssi = float(data.get('rssi'))

            # Insert sensor data into DB tables
            # and retrieve information to control the actuators
            pass
            print(rssi)

            # apply rules to control actuators
            activate = {}
            if rssi:    # both the temperature and humidity reported
                # activate actuators if necessary to control
                if (rssi < 54 ) :
                    activate['buzzer'] = 'ON'
                    buzzer_state = "ON"
                    slack_notify()
                elif (rssi >= 54):
                    activate['buzzer'] = 'OFF'
                    buzzer_state = "OFF"

                else:
                    pass        # nothing to activate actuators

            # reply response message
            response = dict(status=status, deviceid=request.get('deviceid'),
                            msgid=request.get('msgid'))
            if activate:
                response['activate'] = activate
            response = json.dumps(response)
            self.wfile.write(response.encode('utf-8') + b'\n')
            self.wfile.flush()
            logging.debug("%s" % response)

        # end of for loop
        logging.info('Client closing: {}'.format(client))

# rssi renew server
class rssiRenew(socketserver.StreamRequestHandler):
    def handle(self):
        global rssi

        client = self.request.getpeername()
        logging.info("Client connecting: {}".format(client))

        for line in self.rfile:
            # get a request message in JSON and converts into dict
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

            # extract the sensor data from the request
            data = request.get('data')
            if data:        # data exists
                rssi = float(data.get('rssi'))
            
            # reply response message
            response = dict(status=status, deviceid=request.get('deviceid'),
                            msgid=request.get('msgid'))
        
            response = json.dumps(response)
            self.wfile.write(response.encode('utf-8') + b'\n')
            self.wfile.flush()
            logging.debug("%s" % response)

        # end of for loop
        logging.info('Client closing: {}'.format(client))

class note_book_server(socketserver.StreamRequestHandler):
    def handle(self):
        global activate
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
            if activate:
                response['activate'] = True
            else:
                response['activate'] = False
            response = json.dumps(response)
            self.wfile.write(response.encode('utf-8') + b'\n')
            self.wfile.flush()
            print("%s" % response)

        print('Client closing: {}'.format(client))

# logging.basicConfig(filename='', level=logging.INFO)
logging.basicConfig(filename='', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class raspberry_post_server(socketserver.StreamRequestHandler):
    def handle(self):
        global buzzer_state

        client = self.request.getpeername()
        logging.info("Client connecting: {}".format(client))

        for line in self.rfile:
            # get a request message in JSON and converts into dict
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
            activate = {}
            activate["buzzer"] = buzzer_state
            if activate:
                response['activate'] = activate
            response = json.dumps(response)
            self.wfile.write(response.encode('utf-8') + b'\n')
            self.wfile.flush()
            logging.debug("%s" % response)

        # end of for loop
        logging.info('Client closing: {}'.format(client))


def rssi_renew_thread():
    rssi_addr = ("", 8090)
    with socketserver.ThreadingTCPServer(rssi_addr, rssiRenew) as server:
        logging.info('rssi Server starts: {}'.format(rssi_addr))
        server.serve_forever()


def raspberry_post():
    rasp_addr = ("", 8095)
    with socketserver.ThreadingTCPServer(rasp_addr, raspberry_post_server) as server:
        logging.info('rasp Server starts: {}'.format(rasp_addr))
        server.serve_forever()

def server_for_notebook():
    activate = False
    notebook_addr = ("", 5555)
    print("5555")
    if not os.path.exists('data_file.json'):
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

d = threading.Thread(name='rssi', target=rssi_renew_thread)
d.start()

e = threading.Thread(name='rasp', target=raspberry_post)
e.start()

f = threading.Thread(name="notebook", target=server_for_notebook)
f.start()

serv_addr = ("", 10007)
with socketserver.ThreadingTCPServer(serv_addr, IoTRequestHandler) as server:
    logging.info('Server starts: {}'.format(serv_addr))
    server.serve_forever()

