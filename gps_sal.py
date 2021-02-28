import time
import board
import busio 
import adafruit_gps



#uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

#f = open('/home/pi/Project/gps_sal.csv', 'a+')
#if os.stat('/home/pi/Project/gps_sal.csv').st_size == 0:
#    f.write()





gps = adafruit_gps.GPS(uart, debug=False)

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
			
		print("=" * 40)
		print("Latitude: {0:.6f} degrees".format(gps.latitude))
		print("Longitude: {0:.6f} degrees".format(gps.longitude))
		print("Fix quality: {}".format(gps.fix_quality))

# datalogging portion
		
LOG_FILE = "gps_sal.csv"
LOG_MODE = "ab"

with open(LOG_FILE, LOG_MODE) as outfile:
    while True:
	    sentence = gps.readline()
		if not sentence: 
		    continue 
		print(str(sentence, "ascii").strip())
		outfile.write(sentence)
		outfile.flush()
			

