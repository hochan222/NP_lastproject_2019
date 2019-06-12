import socket, json, time, sys
import selectors
import os
import win32evtlog
from time import sleep
import threading
import cv2
import datetime

def getData():
    with open('client_data.json') as outfile:
        data = json.load(outfile)
    return data

def writeData(data):
    with open('client_data.json', 'w') as outfile:
        json.dump(data, outfile)

def lockComp():
    global isLocked
    data = getData()
    try:
        data['lock'] = True
        winpath = os.environ["windir"]
        os.system(winpath + r'\system32\rundll32 user32.dll, LockWorkStation')
    except Exception as e:
        data['lock'] = False
        raise e
    writeData(data)
    isLocked = True


def imageCapture(eventId):
    currentDT = datetime.datetime.now()
    imageName = 'img_', str(eventId) + '.png'
    video_capture = cv2.VideoCapture(False)
    if not video_capture.isOpened():
        raise Exception("Could not open video device")
    ret, frame = video_capture.read()
    cv2.imwrite(imageName, frame)
    print('Image Captured!')
    video_capture.release()
    isCap = False

def checkLogon(dataSet):
    global isLocked, isServer
    last = 0
    lastEvents = []
    login = 0
    server = 'localhost'
    logtype = 'Security'
    while isServer:
        hand = win32evtlog.OpenEventLog(server,logtype)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        events = win32evtlog.ReadEventLog(hand, flags,0)
        eventFive = [event.EventID for event in events[:7]]
        for eventId in eventFive:
            if eventId not in lastEvents:
                if not last == eventId:
                    #print(eventId)
                    if eventId == 4624:
                        print('Login Detected!')
                        isLocked = False
                        data = getData()
                        data['fLock'] = False
                        data['lock'] = False
                        writeData(data)
                        break
                    elif eventId == 4625:
                        print('Login Failed Detected!')
                        try:
                            imageCapture(eventId)
                        except:
                            print("Error: unable to Capture")
                        data = getData()
                        data['fLock'] = True
                        writeData(data)
                        break
                    last = eventId
        lastEvents = eventFive
        print(lastEvents)
        sleep(4)


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
        if timeout_left > False:
            events = self.sel.select(timeout=timeout_left)
            if events:
                return events
        self.time_to_expire += interval
        return []

    def run(self):
        global isLocked, isServer
        msgid = 0

        while True:
            try:
                events = self.select_periodic(interval=5)
                if not events:
                    try:
                        data = getData()
                        if data['lock']:
                            print('lock : True')
                        else:
                            print('lock : False')
                        if data['fLock']:
                            print('fLock : True')
                        else:
                            print('fLock : False')
                    except StopIteration:
                        print('Fail to Get Computer Data')
                        break
                    msgid += True
                    request = dict(method='POST', deviceid=self.deviceid, msgid=msgid, data=data)
                    request_bytes = json.dumps(request).encode('utf-8') + b'\n'
                    self.sock.sendall(request_bytes)
                    self.requests[msgid] = request_bytes
                else:
                    response_bytes = self.rfile.readline()
                    if not response_bytes:
                        self.sock.close()
                        raise OSError('Server abnormally terminated')
                        isServer = False
                    response = json.loads(response_bytes.decode('utf-8'))
                    msgid = response.get('msgid')
                    activate = response.get('noteBookActivate')
                    if msgid and msgid in self.requests:
                        del self.requests[msgid]
                    else:
                        print('{}: illegal msgid received. Ignored'.format(msgid))
                    if activate:
                        if not isLocked:
                            lockComp()
            except Exception as e:
                print(e)
                isServer = False
                break

isServer = True
isLocked = False
if __name__ == '__main__':
    data = {
                'lock': False,
                'fLock': False,
                'image': 0
            }
    with open('client_data.json', 'w') as outfile:
        json.dump(data, outfile)

    host = '13.124.30.140'
    port = 5555
    print(data)
    client = IoTClient((host, port))
    eventHandler = threading.Thread(target=checkLogon, args=(data,))
    eventHandler.start()
    client.run()

    print('Server terminated....')
