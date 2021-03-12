import sys
print (sys.version)

import RPi.GPIO as GPIO
import os
import time, datetime
import board
import busio
import serial
import adafruit_dht
import adafruit_gps

#####################################

#initialize DHT
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

#initialize GPS
pyserial = serial .Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(pyserial, debug=False)

#####################################

variable = (time.strftime('%m-%d-%y'))              # stores date as variable in filename
filename = "/home/pi/Project/" + variable + ".csv"  # to allow new file for each day of recording

if not os.path.exists(filename): #creates logfile if it does not already exist
    f = open(filename, "x")

f = open(filename, 'a+') #appends to logfile 
if os.stat(filename).st_size == 0:
    f.write('  Date    Time    Temp    Humidity    Latitude      Longitude\r\n')

gps.send_command(b"PMTH314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")
last_print = time.monotonic()

running = True
while running:
    try:
        temperature_c = dhtDevice.temperature
#       temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        lat = gps.latitude
        long = gps.longitude


        gps.update()
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            if not gps.has_fix:
                print("waiting for fix")
                continue

        print("=" * 125)
        print("Date: {0}    Time: {1}    Temp: {2} C    RH: {3}%    Lat: {4} deg    Lon: {5} deg ".format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature_c, humidity, lat, long))
        print("=" * 125)

        if temperature_c is not None and humidity is not None and lat is not None and long is not None:
            f.write('{0}, {1}, {2:.1f}*C, {3:.1f} %, {4:.6f} deg, {5:.6f} deg\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature_c, humidity, lat, long))
            #f.write('{0}, {1}, {2:.1f} C, {3:.1f}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature_c, humidity))
        time.sleep(5)


    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except KeyboardInterrupt:
        print("program stopped")
        running = False
        f.close()
