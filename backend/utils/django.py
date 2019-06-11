import socket, sys
import socketserver, json, selectors
import logging
import threading
import time

# main: 10007, rssi_renew_thread: 8090
# raspberry: 8095

rssi = 0

# django main server
class IoTRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
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
                if (rssi > 50 ) :
                    activate['buzzer'] = 'ON'
                    
                    # django >>> raspberry socket
                    client = raspberryIoTClient(("127.0.0.1", 8095), 99, 'ON')
                    client.run()
                elif (rssi <= 50):
                    activate['buzzer'] = 'OFF'

                    client = raspberryIoTClient(("127.0.0.1", 8095), 99, 'OFF')
                    client.run()
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








# raspberry pi buzzer
class raspberryIoTClient:
    def __init__(self, server_addr, deviceid, status_of):
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
        self.status = status_of

    def run(self):
        # Report sensors' data forever
        msgid = 0

        try:      # timeout occurs
            data = dict(buzzer=self.status)
            # msgid = str(uuid.uuid1())
            msgid += 1
            request = dict(method='POST', deviceid=self.deviceid, msgid=msgid, data=data)
            logging.debug(request)
            request_bytes = json.dumps(request).encode('utf-8') + b'\n'
            self.sock.sendall(request_bytes)
            self.requests[msgid] = request_bytes
        except:               # EVENT_READ
            response_bytes = self.rfile.readline()     # receive response
            if not response_bytes:
                self.sock.close()
                raise OSError('Server abnormally terminated')
            response = json.loads(response_bytes.decode('utf-8'))
            logging.debug(response)

            # msgid in response allows to identify the specific request message
            # It enables asynchronous transmission of request messages in pipelining
            msgid = response.get('msgid')
            if msgid and msgid in self.requests:
                del self.requests[msgid]
            else:
                logging.warning('{}: illegal msgid received. Ignored'.format(msgid))
     
        # end of while loop

        logging.info('raspberry client terminated')
        self.sock.close()


# logging.basicConfig(filename='', level=logging.INFO)
logging.basicConfig(filename='', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def rssi_renew_thread():
    rssi_addr = ("", 8090)
    with socketserver.ThreadingTCPServer(rssi_addr, IoTRequestHandler) as server:
        logging.info('rssi Server starts: {}'.format(rssi_addr))
        server.serve_forever()

d = threading.Thread(name='rssi', target=rssi_renew_thread)
d.start()

serv_addr = ("", 10007)
with socketserver.ThreadingTCPServer(serv_addr, IoTRequestHandler) as server:
    logging.info('Server starts: {}'.format(serv_addr))
    server.serve_forever()

