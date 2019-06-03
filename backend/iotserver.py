import socketserver, json
import logging
# import time
from datetime import date, time, datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
django.setup()

from post.models import IoT_home

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
                temperature = float(data.get('temperature'))
                humidity = float(data.get('humidity'))

            # Insert sensor data into DB tables
            # and retrieve information to control the actuators
            print(temperature, humidity)
            pass
            print(IoT_home.objects.all())
            now_time = '{0.year:04}{0.month:02}{0.day:02}{0.hour}{0.minute}'.format(datetime.now())
            IoT_home(time=int(now_time), temperature=temperature, humidity=humidity).save()
            # apply rules to control actuators
            activate = {}
            if temperature and humidity:    # both the temperature and humidity reported
                # activate actuators if necessary to control
                if (temperature >= 32 and humidity >= 70) \
                        or (temperature >= 34) \
                        or (temperature >= 30 and humidity >= 90):
                    activate['aircon'] = 'ON'
                elif (temperature < 28 or humidity < 50):
                    activate['aircon'] = 'OFF'
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

# logging.basicConfig(filename='', level=logging.INFO)
logging.basicConfig(filename='', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

serv_addr = ("", 10007)
with socketserver.ThreadingTCPServer(serv_addr, IoTRequestHandler) as server:
    logging.info('Server starts: {}'.format(serv_addr))
    server.serve_forever()

