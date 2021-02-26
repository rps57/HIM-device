# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

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

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# open pre-made file for data logs
try:
    f = open('/home/pi/HIM-device/dht22_logging.csv', 'a+') # this file may need to change
    if os.stat('/home/pi/HIM-device/dht22_logging.csv').st_size == 0:
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




################### GPS location collection ###################

#uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

gps.send_command(b"PMTK220, 1000")

last_print = time.monotonic()
while True:
    gps.update()
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print("Waiting for fix")
            continue
        #print("=" * 40)
        
        print("Latitude: {0:.6f} degrees".format(gps.latitude))
        print("Longitude: {0:.6f} degrees".format(gps.longitude))
        print("Fix quality: {}".format(gps.fix_quality))
        
                    
######################## GPS datalogging ########################		

LOG_FILE = "gps.txt" #change to same file as T/H logging after testing functionality 
LOG_MODE = "ab"

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart)


with open(LOG_FILE, LOG_MODE) as outfile:
    while True:
        sentence = gps.readline()
        if not sentence:
            continue
        print(str(sentence, "ascii").strip())
        outfile.write(sentence)
        outfile.flush()	