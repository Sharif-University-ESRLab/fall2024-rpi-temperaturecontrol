import sys
sys.path.append('env/lib/python3.8/site-packages')

from gpiozero import LED
from time import sleep


# Define the GPIO pin (BCM numbering)
led = LED(17)

while True:
    led.on()  # Set pin HIGH
    print("Pin set to HIGH")
    sleep(1)  # Wait for 1 second

    led.off()  # Set pin LOW
    print("Pin set to LOW")
    sleep(1)  # Wait for 1 second
