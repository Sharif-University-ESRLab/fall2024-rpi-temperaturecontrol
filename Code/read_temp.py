import time
import board
import adafruit_dht

# Initialize DHT device, with data pin connected to board.D4 (GPIO4 on Pi)
# For an AM2302/DHT22 sensor:
dhtDevice = adafruit_dht.DHT22(board.D4)

while True:
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        if humidity is not None and temperature_c is not None:
            print(f"Temp: {temperature_c:.1f} °C   Humidity: {humidity:.1f}%")
        else:
            print("Failed to retrieve data from the DHT sensor")
    except RuntimeError as error:
        # It's normal to get errors occasionally, sensor may be busy.
        print(f"Reading error: {error.args[0]}")
    time.sleep(2)