# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import sys
print (sys.version)

import time
import board
import adafruit_dht

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



