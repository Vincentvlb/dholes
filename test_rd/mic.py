import pyaudio
import wave
import struct
import math
import time

def get_mic_id() -> int:
    p = pyaudio.PyAudio()
    for mic_id in range(p.get_device_count()):
        if "USB Audio Device" in p.get_device_info_by_index(mic_id).get('name'):
            return mic_id
    return None

print(get_mic_id())
dev_index = 0
channels = 1
format = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
wav_output_filename = 'test1.wav'

audio = pyaudio.PyAudio()

samp_rate = int(audio.get_device_info_by_index(dev_index).get('defaultSampleRate'))

stream = audio.open(format = format,rate = samp_rate,channels = channels, input_device_index = dev_index,input = True, frames_per_buffer=1024)
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
    file = open("frames.txt", "w+")
    print("Start recording, for stop the record press ctrl+c on time.")
    cpt=0
    start_time = time.time();
    while True:
        data = stream.read(2048, exception_on_overflow = False)
        frames.append(data)
        file.write(f"{time.time()-start_time};{get_rms(data)} \n")
        cpt+=1
        print(get_rms(data)*10)
except KeyboardInterrupt:
    print("Finished recording")
finally:
    print("Save record...")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(channels)
    wavefile.setsampwidth(audio.get_sample_size(format))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    file.close()
