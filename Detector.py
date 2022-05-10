import threading
import pyaudio
import struct
import math
from typing import Callable
import multiprocessing

class Detector():

    def __init__(self, fct_on_detection: Callable):
        self.__working = False
        self._fct_on_detection = fct_on_detection
        ctx = multiprocessing.get_context('spawn')
        self._queue = ctx.Queue()
        self._thread = threading.Thread(target=self._running_method, args=(self._queue,))

    def start_detection(self):
        self.__working = True
        self._thread.start()

    def stop_detection(self):
        self.__working = False
        self._thread.join()

    def is_working(self) -> bool:
        return self.__working

    def _running_method(self, queue: multiprocessing.Queue):
        raise NotImplementedError("Subclass must implement abstract method")

class AudioDetector(Detector):

    def __init__(self, fct_on_detection: Callable, input_device_index):
        super().__init__(fct_on_detection)
        self.__audio = pyaudio.PyAudio() 
        self.__audio_format = pyaudio.paInt16
        self.__input_device_index = input_device_index
        self.__channels = 1
        self.__frames_per_buffer = 2048
        self.__samp_rate = int(self.__audio.get_device_info_by_index(self.__input_device_index).get('defaultSampleRate'))
        self.__detection_threshold = None
        self.__short_normalize = (1.0/32768.0)
        

    def __get_rms(self, block):
        count = len(block)/2
        unpack_format = "%dh"%(count)
        shorts = struct.unpack(unpack_format, block)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * self.__short_normalize
            sum_squares += n*n
        return math.sqrt(sum_squares/count)*1000

    def start_detection(self):
        if self.__detection_threshold is None:
            raise Exception("Couldn't start detection because detection threshold isn't define.")
        self.__stream = self.__audio.open(  format = self.__audio_format, \
                                            rate = self.__samp_rate, \
                                            channels = self.__channels, \
                                            input_device_index = self.__input_device_index, \
                                            frames_per_buffer=self.__frames_per_buffer, \
                                            input = True)
        super().start_detection()

    def set_threshold(self, detection_threshold: float):
        self.__detection_threshold = detection_threshold
        self._queue.put(detection_threshold)
        while not self._queue.empty():
            continue
        return f'{self.__detection_threshold:.0f}'

    def get_formatted_threshold(self):
        return f'{self.__detection_threshold:.0f}'

    def _running_method(self, queue: multiprocessing.Queue):
        detection_threshold = queue.get()
        while self.is_working():
            if not queue.empty():
                detection_threshold = queue.get()
                print("new_threshold:",detection_threshold)
            data = self.__stream.read(2048, exception_on_overflow = False)
            if self.__get_rms(data) > detection_threshold:
                self._fct_on_detection()
            