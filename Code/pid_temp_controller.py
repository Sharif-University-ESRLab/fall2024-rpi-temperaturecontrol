import os, sys
sys.path.append('env/lib/python3.8/site-packages')

import time
import board
import adafruit_dht as adht
from gpiozero import PWMOutputDevice

SETPOINT_TEMPERATURE = 24.0  # in Celsius

# PID parameters (start small, tune as needed)
Kp = 0.04
Ki = 0.001
Kd = 1

FAN_PWM_PIN = 23
PWM_FREQUENCY = 100

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
            print("error reading temp, using default")
            return last_temp
    except Exception as e:
        print("error reading temp, using default, error:", str(e))
        
        return last_temp



# Create PWM output device
fan_pwm = PWMOutputDevice(FAN_PWM_PIN, frequency=PWM_FREQUENCY, initial_value=0.0)

integral_error = 0.0
previous_error = 0.0
previous_time = time.time()

while True:
    temperature = get_temperature()
    current_time = time.time()
    dt = current_time - previous_time
    
    if temperature is not None and dt > 0:
        error = temperature - SETPOINT_TEMPERATURE
        
        # Integral term
        integral_error += error * dt
        
        # Derivative term
        derivative_error = (error - previous_error) / dt
        
        # PID output
        pid_output = (Kp * error) + (Ki * integral_error) + (Kd * derivative_error)
        
        # Convert PID output => 0..1 duty cycle
        # You might clamp this between 0..1
        if pid_output < 0:
            pid_output = 0
        elif pid_output > 1:
            pid_output = 1
        
        # Set PWM
        fan_pwm.value = pid_output
        
        # Debug prints
        print(f"Temp: {temperature:.2f}C, Error: {error:.2f}, PID out: {pid_output:.2f}")
        
        # Prepare for next iteration
        previous_error = error
        previous_time = current_time
    else:
        print("Failed to read DHT22 or dt=0, skipping this iteration.")
    
    # Adjust delay as needed, but typically a 1-2 second loop is fine for basic fan control
    time.sleep(1)
