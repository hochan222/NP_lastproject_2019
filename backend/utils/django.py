import socket, sys
import socketserver, json, selectors
import logging
import threading
import time

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
                if (rssi < 60 ) :
                    activate['buzzer'] = 'ON'
                    buzzer_state = "ON"

                elif (rssi >= 60):
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

d = threading.Thread(name='rssi', target=rssi_renew_thread)
d.start()

e = threading.Thread(name='rasp', target=raspberry_post)
e.start()

serv_addr = ("", 10007)
with socketserver.ThreadingTCPServer(serv_addr, IoTRequestHandler) as server:
    logging.info('Server starts: {}'.format(serv_addr))
    server.serve_forever()

