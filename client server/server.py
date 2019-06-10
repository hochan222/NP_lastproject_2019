import socketserver, json
import logging
import os

class IoTRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = self.request.getpeername()
        print("Client connecting: {}".format(client))

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
                print(error_msg)
                break
            else:
                status = 'OK'
                print("{}:{}".format(client, request))

            # extract the sensor data from the request
            data = request.get('data')
            if data:        # data exists
                lock = data.get('lock')
                fLock = data.get('fLock')

            with open("data_file.json", "w") as write_file:
                json.dump(data, write_file)

            if lock:
                print('Windows is locked!')

            if fLock:
                print('Logon failed ditected!')

            # reply response message
            response = dict(status=status, deviceid=request.get('deviceid'),
                            msgid=request.get('msgid'))
            response = json.dumps(response)
            self.wfile.write(response.encode('utf-8') + b'\n')
            self.wfile.flush()
            print("%s" % response)

        # end of for loop
        print('Client closing: {}'.format(client))

if __name__ == '__main__':

    if not os.path.exists('data_file.json'):
        data = {
                'lock': '0',
                'fLock': '0'
            }
        with open('data_file.json', 'w') as outfile:
            json.dump(data, outfile)

    serv_addr = ("10.10.1.236", 5555)
    with socketserver.ThreadingTCPServer(serv_addr, IoTRequestHandler) as server:
        print('Server starts: {}'.format(serv_addr))
        server.serve_forever()

