import pyaudio
import wave
import struct
import math
import time

threshold = 2
number_picture = 30

dev_index = 1
channels = 1
format = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)

audio = pyaudio.PyAudio()

samp_rate = int(audio.get_device_info_by_index(dev_index).get('defaultSampleRate'))

stream = audio.open(format = format,rate = samp_rate,channels = channels, input_device_index = dev_index,input = True, frames_per_buffer=2048)
frames = []

def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

try:
    print("Start, for stop press ctrl+c on time.")
    cpt=-1
    nb_picture=0
    start_time = time.time();
    while True:
        data = stream.read(2048)
        if get_rms(data)*10> threshold:
            if cpt>0:
                print(f"Add {number_picture} pictures.")
                cpt+= number_picture
            elif cpt==-1:
                print(f"Start record {number_picture} pictures.")
                cpt = number_picture
        if cpt >0:
            #Take picture
            cpt-=1
            nb_picture+=1
        elif cpt==0:
            print(f"Record of pictures are finish with {nb_picture} pictures.")
            cpt=-1
            nb_picture=0

except KeyboardInterrupt:
    print("Finished, close...")
finally:
    print("Save record...")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()
