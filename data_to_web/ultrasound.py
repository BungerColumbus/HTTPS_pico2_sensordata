from machine import Pin, time_pulse_us
import time

def get_distance(echo, trig):
    trig.value(0)
    time.sleep_us(2)
    
    # send a 10-microsecond HIGH pulse to trigger the sensor
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    time.sleep_us(10)

    print("wawawa")
    # measures the duration of the incoming pulse on the ECHO pin
    # time_pulse_us returns the pulse length in microseconds
    pulse_time = time_pulse_us(echo, 1, 30000) # 30ms timeout (max range)
        


    # calculations in order to see the actual distance based on the time it took for sound
    distance_cm = (pulse_time * 0.0343) / 2
    
    return distance_cm