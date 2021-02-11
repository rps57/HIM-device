import sys
print (sys.version)

import os
import time
import board
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# open pre-made file for data logs
try:
    f = open('/home/pi/dht22_logging.csv', 'a+')
    if os.stat('/home/pi/dht22_logging.csv').st_size == 0:
            f.write('Date,Time,Temperature,Humidity\r\n')
# do nothing			
except:
    pass

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)


	# if data is collected, store it
    if humidity is not None and temperature is not None:
       f.write('{0},{1},{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity)) 
    else:
        print("Failed to retrieve data from humidity sensor")

    time.sleep(20)
