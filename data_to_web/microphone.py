import machine
import network
import time
import struct
import gc
import array  # Needed for 16-bit memory arrays

RECORD_TIME_SEC = 5       
SAMPLE_RATE = 8000        # Keep this at 8000 for stability
ADC_PIN = 28              
FILENAME = "recording.wav"

# Setup ADC
mic = machine.ADC(ADC_PIN)

def create_wav_header(sample_rate, bits_per_sample, num_samples):
    """
    Generates a standard 44-byte RIFF/WAVE header.
    """
    byte_rate = (sample_rate * bits_per_sample * 1) // 8
    block_align = (bits_per_sample * 1) // 8
    data_size = (num_samples * bits_per_sample * 1) // 8
    file_size = data_size + 36

    header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF',
        file_size,
        b'WAVE',
        b'fmt ',
        16,                # Subchunk1Size (16 for PCM)
        1,                 # AudioFormat (1 for uncompressed PCM)
        1,                 # NumChannels (1 for Mono)
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b'data',
        data_size
    )
    return header

def record_audio():
    try:
        psm_pin = machine.Pin("WL_GPIO1", machine.Pin.OUT)
        psm_pin.value(1)
    except Exception as e:
        print("Could not set WL_GPIO1:", e)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    
    
    num_samples = SAMPLE_RATE * RECORD_TIME_SEC
    
    # NEW: Create an array of signed 16-bit integers ('h' format)
    audio_buffer = array.array('h', [0] * num_samples)
    sample_interval_us = int(1000000 / SAMPLE_RATE)
    
    print("Recording started... Speak into the mic!")
    
    gc.collect()
    gc.disable() 
    
    start_time = time.ticks_us()
    next_sample_time = start_time
    
    for i in range(num_samples):
        while time.ticks_diff(time.ticks_us(), next_sample_time) < 0:
            pass
            
        # NEW: The Pico reads 0 to 65535. 16-bit WAV files expect -32768 to 32767.
        # We subtract 32768 to center the audio at 0.
        audio_buffer[i] = mic.read_u16() - 32768
        
        next_sample_time = time.ticks_add(next_sample_time, sample_interval_us)
        
    gc.enable() 
    
    print("Recording finished. Saving to {}...".format(FILENAME))
    
    with open(FILENAME, "wb") as f:
        # Pass 16 as the bits_per_sample
        f.write(create_wav_header(SAMPLE_RATE, 16, num_samples))
        # Write the 16-bit array directly to the file
        f.write(audio_buffer)
        
    print("File saved successfully!")
