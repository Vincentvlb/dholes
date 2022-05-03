import threading
import pyaudio
import struct
import math

class Detector():

    def __init__(self, fct_on_detection):
        self.__working = False
        self.__fct_on_detection = fct_on_detection
        self.__thread = threading.Thread(target=self.__running_method)

    def start_detection(self):
        self.__working = True
        self.__thread.start()

    def stop_detection(self):
        self.__working = False
        self.__thread.join()

    def is_working(self) -> bool:
        return self.__working

    def __running_method(self):
        raise NotImplementedError("Subclass must implement abstract method")

class AudioDetector(Detector):

    def __init__(self, fct_on_detection):
        Detector.__init__(fct_on_detection)
        self.__audio = pyaudio.PyAudio() 
        self.__audio_format = pyaudio.paInt16
        self.__input_device_index = 1
        self.__channels = 1
        self.__frames_per_buffer = 2048
        self.__samp_rate = int(self.__audio.get_device_info_by_index(self.__input_device_index).get('defaultSampleRate'))
        self.__detection_threshold = None
        self.__short_normalize = (1.0/32768.0)

    def __get_rms(block):
        count = len(block)/2
        unpack_format = "%dh"%(count)
        shorts = struct.unpack(unpack_format, block)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * self.__short_normalize
            sum_squares += n*n
        return math.sqrt(sum_squares/count)*10

    def start_detection(self):
        if self.__detection_threshold is None:
            raise Exception("Couldn't start detection because detection threshold isn't define.")
        self.__stream = self.__audio.open(  format = self.__audio_format, \
                                            rate = self.__samp_rate, \
                                            channels = self.__channels, \
                                            input_device_index = self.__input_device_index, \
                                            frames_per_buffer=self.self.__frames_per_buffer, \
                                            input = True)
        super().start_detection()

    def set_detection_threshold(self, detection_threshold: float):
        self.__detection_threshold = detection_threshold

    def __running_method(self):
        while self.__working:
            data = stream.read(2048)
            if self.__get_rms(data) > self.__detection_threshold:
                self.__fct_on_detection()
