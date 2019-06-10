import socket, json, time, sys
import os

def getData():
    with open('data_file.json') as outfile:
        data = json.load(outfile)
    return data

def writeData(data):
    with open('data_file.json', 'w') as outfile:
        json.dump(data, outfile)

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

    def run(self):
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
                    writeData(response.get('data'))
                    if msgid and msgid in self.requests:
                        del self.requests[msgid]
                    else:
                        print('{}: illegal msgid received. Ignored'.format(msgid))
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
    client.run()
