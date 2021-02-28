import sys
print (sys.version)

import os
import time
import board
import busio
import serial
import adafruit_dht
import adafruit_gps


################### DHT22 temp/humidity collection ###################

# initialize dht device 
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

try:
    f = open('/home/pi/HIM-device/dht22_logging.csv', 'a+') # this file may need to change
    if os.stat('/home/pi/HIM-device/dht22_logging.csv').st_size == 0:
            f.write('Date,Time,Temperature,Humidity\r\n')


while True:
    try:
        # print values to serial port 
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    # time between samples
    time.sleep(3.0)
    
    

################### Temperature and humidity datalogging ###################

#DHT_SENSOR = Adafruit_DHT.DHT22
#DHT_PIN = 4

# open pre-made file for data logs
#try:
#    f = open('/home/pi/HIM-device/dht22_logging.csv', 'a+') # this file may need to change
#    if os.stat('/home/pi/HIM-device/dht22_logging.csv').st_size == 0:
#            f.write('Date,Time,Temperature,Humidity\r\n')
# do nothing			
#except:
#    pass

#while True:
#    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)


    # if data is collected, store it
#    if humidity is not None and temperature is not None:
#       f.write('{0},{1},{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity)) 
#    else:
#        print("Failed to retrieve data from humidity sensor")

#    time.sleep(20)