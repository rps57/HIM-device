import sys
print (sys.version)

import os
import time
import board
import busio
import adafruit_dht

dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

f = open('/home/pi/Project/dht22_sal.csv', 'a+') # this file may need to change
if os.stat('/home/pi/Project/dht22_sal.csv').st_size == 0:
    f.write('Date,Time,Temperature,Humidity\r\n')
running = True
while running:

    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity

        print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))

        if humidity is not None and temperature_c is not None:
            f.write('{0},{1},{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature_c, humidity))
            time.sleep(3)


        else:
            print("failed to read sensor")

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except KeyboardInterrupt:
        print("Program stopped")
        running = False
        f.close()
