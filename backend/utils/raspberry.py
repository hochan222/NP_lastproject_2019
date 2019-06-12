"""
We define IoT Protocol messages as Python dicts for example.
They are serialized as JSON format string, then encoded in utf-8.
Caution: because every messages are delimited by new line character (b'\n') in a TCP session,
avoid using LF character inside Python strings.

The POST request messages may be sent periodically
for server to inform the client to activate the actuators if needed.

<request message> ::= <request object in JSON format with UTF-8 encoding> <LF>

<request object> ::=
    {   'method': 'POST',
        'deviceid': <device id>,
        'msgid': <messge id>,
        'data': {'temperature': 28.5, 'humidity': 71},
    }

<response message> ::= <response object in JSON format with UTF-8 encoding> <LF>

<response object> ::=
    {   'status': 'OK' | 'ERROR <error msg>',
        'deviceid': <device id>
        'msgid': <messge id>
      [ 'activate': {'aircon': 'ON', 'led': 'OFF' } ]  # optional
    }

<LF> ::= b'\n'
"""
import SocketServer as socketserver
import socket, json, time, sys
import uuid
import selectors34 as selectors
import random, math
import threading
import logging
import RPi.GPIO as GPIO

# print uuid.uuid4()

Buzzer = 11 

def setup(pin):
	global BuzzerPin
	BuzzerPin = pin
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(BuzzerPin, GPIO.OUT)

def on():
	GPIO.output(BuzzerPin, GPIO.HIGH)

def off():
	GPIO.output(BuzzerPin, GPIO.LOW)

class IoTClient:
    def __init__(self, server_addr, deviceid):
        """IoT client with persistent connection
        Each message separated by b'\n'

        :param server_addr: (host, port)
        :param deviceid: id of this IoT
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_addr)  # connect to server process
        rfile = sock.makefile('rb')  # file-like obj
        sel = selectors.DefaultSelector()
        sel.register(sock, selectors.EVENT_READ)

        self.sock = sock
        self.rfile = rfile
        self.deviceid = deviceid
        self.sel = sel
        self.requests = {}      # messages sent but not yet received their responses
        self.time_to_expire = None

    def select_periodic(self, interval):
        """Wait for ready events or time interval.
        Timeout event([]) occurs every interval, periodically.
        """
        now = time.time()
        if self.time_to_expire is None:
            self.time_to_expire = now + interval
        timeout_left = self.time_to_expire - now
        if timeout_left > 0:
            events = self.sel.select(timeout=timeout_left)
            if events:
                return events
        # time to expire elapsed or timeout event occurs
        self.time_to_expire += interval  # set next time to expire
        return []

    def run(self):
        msgid = 0

        while True:
            try:
                events = self.select_periodic(interval=5)
                if not events:      # timeout occurs
                    # msgid = str(uuid.uuid1())
                    msgid += 1
                    request = dict(method='POST', deviceid=self.deviceid, msgid=msgid, data="")
                    request_bytes = json.dumps(request).encode('utf-8') + b'\n'
                    self.sock.sendall(request_bytes)
                    self.requests[msgid] = request_bytes
                    print("1")
                else:               # EVENT_READ
                    response_bytes = self.rfile.readline()     # receive response
                    print("2")
                    if not response_bytes:
                        self.sock.close()
                        raise OSError('Server abnormally terminated')
                    response = json.loads(response_bytes.decode('utf-8'))

                    # msgid in response allows to identify the specific request message
                    # It enables asynchronous transmission of request messages in pipelining
                    msgid = response.get('msgid')
                    buzzer_state = response.get('activate')["buzzer"]
                    print(buzzer_state)
                    if buzzer_state == "ON":
                        print("on")
                        on()
                        time.sleep(1)
                        off()
                    elif buzzer_state == "OFF":
                        print("off")
                        off()

                    if msgid and msgid in self.requests:
                        del self.requests[msgid]
            except Exception as e:
                break
        # end of while loop

        self.sock.close()

if __name__ == '__main__':
    print("1")
    setup(Buzzer)
    print("2")
    client = IoTClient(("13.209.76.226", 8095),2323)
    client.run()
