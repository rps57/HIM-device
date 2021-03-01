import time
import board
import busio 
import adafruit_gps
import serial 
import os

pyserial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(pyserial, debug=False)

f = open('/home/pi/Project/gps_sal.csv', 'a+')
if os.stat('/home/pi/Project/gps_sal.csv').st_size == 0L
    f.write('Date	Time	Latitude	Longtiude\r\n')

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

gps.send_command(b"PMTK220,1000")
last_print = time.monotonic()
while True: 
    gps.update()
	current = time.monotonic()
	if current - last_print >= 1.0:
	    last_print = current
		if not gps.has_fix:
		    print("waiting for fix")
			continue 
			
		print("=" * 90)
		print("Date: {0}    Time: {1}    Latitude: {2:.6f} degrees    Longitude: {3:.6f}   Fix Quality: {} ".format(
		    time.strftime('%m/%d/%y'), time.strftime('%H:%M'), gps.latitude, gps.longitude, gps.fix_quality)
			
			)
		print("=" * 90)
				
		if gps.latitude is not None and gps.longitude is not None:
		    f.write(
			    '{0},{1},{2:.6f} degrees, {3:.6f} degrees\r\n'.format(time.strftime('%m/%d/%y'), 
				time.strftime('%H:%M'), gps.latitude, gps.longitude)
				
				)
				
				
				
				
				


			

