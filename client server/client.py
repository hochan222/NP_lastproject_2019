import socket, json, time, sys
import os
import win32evtlog
from time import sleep
import threading
import cv2
import datetime

def getData():
    with open('data_file.json') as outfile:
        data = json.load(outfile)
    return data

def writeData(data):
    with open('data_file.json', 'w') as outfile:
        json.dump(data, outfile)

def lockComp():
    winpath = os.environ["windir"]
    os.system(winpath + r'\system32\rundll32 user32.dll, LockWorkStation')

def imageCapture(eventId):
    global isCap
    currentDT = datetime.datetime.now()
    imageName = 'img_', str(eventId) + '.png'
    video_capture = cv2.VideoCapture(0)
    # Check success
    if not video_capture.isOpened():
        raise Exception("Could not open video device")
    # Read picture. ret === True on success
    ret, frame = video_capture.read()
    cv2.imwrite(str(eventId) + currentDT.strftime("_%Y%m%d%H%M%S") + '.png',frame)
    # Close device
    video_capture.release()
    isCap = False

def checkLogon():
    global isCap
    login = 0
    server = 'localhost'
    logtype = 'Security'
    hand = win32evtlog.OpenEventLog(server,logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    events = win32evtlog.ReadEventLog(hand, flags,0)
    event = events[0]
    print(event.EventID)
    if event.EventID == 4625:
        print('Login Failed Detected!')
        try:
            if not isCap:
                handler = threading.Thread(target=imageCapture, args=(event.EventID,))
                handler.setDaemon(True)
                handler.start()
            isCap = True
        except:
            print("Error: unable to start thread")
        login = 1
        return login
    if event.EventID == 4624:
        print('Login Detected!')
        return

class IoTClient:
    def __init__(self, server_addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_addr)
        rfile = sock.makefile('rb')
        sel = selectors.DefaultSelector()
        sel.register(sock, selectors.EVENT_READ)

        self.sock = sock
        self.rfile = rfile
        self.sel = sel
        self.deviceid = 'Windows_10'
        self.requests = {}
        self.time_to_expire = None

    def select_periodic(self, interval):
        now = time.time()
        if self.time_to_expire is None:
            self.time_to_expire = now + interval
        timeout_left = self.time_to_expire - now
        if timeout_left > 0:
            events = self.sel.select(timeout=timeout_left)
            if events:
                return events
        self.time_to_expire += interval
        return []

    def run(self, data):
        msgid = 0

        while True:
            try:
                events = self.select_periodic(interval=5)
                if not events:
                    try:
                        data = getData()
                    except StopIteration:
                        print('Fail to Get Computer Data')
                        break
                    msgid += 1
                    request = dict(method='POST', deviceid=self.deviceid, msgid=msgid, data=data)
                    request_bytes = json.dumps(request).encode('utf-8') + b'\n'
                    self.sock.sendall(request_bytes)
                    self.requests[msgid] = request_bytes
                else:
                    response_bytes = self.rfile.readline()
                    if not response_bytes:
                        self.sock.close()
                        raise OSError('Server abnormally terminated')
                    response = json.loads(response_bytes.decode('utf-8'))
                    msgid = response.get('msgid')
                    activate = response.get('activate')
                    if msgid and msgid in self.requests:
                        del self.requests[msgid]
                    else:
                        print('{}: illegal msgid received. Ignored'.format(msgid))
                    if activate:
                        lockComp()
            except Exception as e:
                print(e)
                break

if __name__ == '__main__':

    if not os.path.exists('data_file.json'):
        data = {
                'lock': '0',
                'fLock': '0'
            }
        with open('data_file.json', 'w') as outfile:
            json.dump(data, outfile)

    host = '10.10.1.236'
    port = 5555
    print(data)
    client = IoTClient((host, port))
    try:
        clientHandler = threading.Thread(target=client.run, args=(data,))
        clientHandler.setDaemon(True)
        clientHandler.start()
    except Exception as e:
        raise e
