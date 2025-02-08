import os, sys
sys.path.append('env/lib/python3.8/site-packages')

import time
import board
import adafruit_dht as adht
from gpiozero import LED

SETPOINT_TEMPERATURE1 = 26.0  # in Celsius

SETPOINT_TEMPERATURE2 = 27.0  # in Celsius

FAN_PIN = 23
dht_device = adht.DHT22(board.D4)
last_temp = SETPOINT_TEMPERATURE1

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

current_state = 0

while True:
    temperature = get_temperature()
    
    if temperature > SETPOINT_TEMPERATURE2:
        current_state = 1
    elif temperature < SETPOINT_TEMPERATURE1:
        current_state = 0
    
    fan_is_on = current_state
    
    print(f"Temp: {temperature:.2f}C, Fan's state: {'On' if fan_is_on else 'Off'}")

    if fan_is_on:
       fan_controller.on()
    else:
       fan_controller.off()

    time.sleep(1)
