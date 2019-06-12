import math

txPower = -69
rssi = -60

dist = math.pow(10, ((txPower - rssi)/(10*2)))
print(dist)

