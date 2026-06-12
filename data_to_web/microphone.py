import machine
import time

mic = machine.ADC(28)

# ADC reads values from 0 to 65535 (16-bit), VBUS is 5V
CONVERSION_FACTOR = 5 / 65535

def sample_microphone(sample_window_ms=50):
    """
    Reads the microphone for a given time window and 
    returns the peak-to-peak voltage.
    """
    start_time = time.ticks_ms()
    
    # Set initial min/max to extreme opposites
    signal_max = 0
    signal_min = 65535
    
    # Sample the analog signal rapidly for the duration of the window
    while time.ticks_diff(time.ticks_ms(), start_time) < sample_window_ms:
        sample = mic.read_u16()
        
        if sample < 65535:
            if sample > signal_max:
                signal_max = sample
            if sample < signal_min:
                signal_min = sample

    peak_to_peak = signal_max - signal_min
    
    # Convert the raw ADC value to Volts
    volts = peak_to_peak * CONVERSION_FACTOR
    return volts