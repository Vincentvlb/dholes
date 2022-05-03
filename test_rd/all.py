import pyaudio
import wave
import struct
import math
import time
import subprocess

sound_threshold = 2

#Vidéos param :
video_time = 5
width = 1920
height = 1080
framerate = 30

dev_index = 1
channels = 1
format = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)

audio = pyaudio.PyAudio()

samp_rate = int(audio.get_device_info_by_index(dev_index).get('defaultSampleRate'))

stream = audio.open(format = format,rate = samp_rate,channels = channels, input_device_index = dev_index,input = True, frames_per_buffer=2048)

def get_rms( block ):
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

try:

    print("Start, for stop press ctrl+c.")
    start_time = time.time();
    while True:
        data = stream.read(2048)
        if get_rms(data)*10> sound_threshold:
            subprocess.run(f"ffmpeg -f v4l2 -r {framerate} -s {width}x{height} -t {video_time} -i /dev/video0 videos/recording.avi", shell=True, check=True)

except KeyboardInterrupt:
    print("Finished, close...")
finally:
    print("Save record...")

    stream.stop_stream()
    stream.close()
    audio.terminate()
