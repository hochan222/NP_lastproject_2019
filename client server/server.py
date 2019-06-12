import socketserver, json
import logging
import os
import cv2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class IoTRequestHandler(socketserver.StreamRequestHandler):
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

            with open(os.path.join(BASE_DIR, 'server_data.json'), "w") as write_file:
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

activate = False
if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    if not os.path.exists('server_data.json'):
        data = {
                'lock': False,
                'fLock': False,
                'image': 0
            }
        with open(os.path.join(BASE_DIR, 'server_data.json'), 'w') as outfile:
            json.dump(data, outfile)

    serv_addr = ("192.168.0.27", 5555)
    with socketserver.ThreadingTCPServer(serv_addr, IoTRequestHandler) as server:
        print('Server starts: {}'.format(serv_addr))
        server.serve_forever()

    print('Server Done This is thread~')
