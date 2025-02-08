import os, sys
sys.path.append('env/lib/python3.8/site-packages')

import time
import board
import adafruit_dht as adht
from gpiozero import LED

SETPOINT_TEMPERATURE = 24.0  # in Celsius

FAN_PIN = 23
dht_device = adht.DHT22(board.D4)
last_temp = SETPOINT_TEMPERATURE

def get_temperature():
    global dht_device, last_temp

    try:
        temperature = dht_device.temperature
        if temperature is not None:
            last_temp = temperature
            return temperature
        else:
            return last_temp
    except Exception as _:
        return last_temp

fan_controller = LED(FAN_PIN)

while True:
    temperature = get_temperature()
    
    fan_is_one = temperature > SETPOINT_TEMPERATURE
    
    print(f"Temp: {temperature:.2f}C, Fan's state: {'On' if fan_is_one else 'Off'}")
    
    time.sleep(1)