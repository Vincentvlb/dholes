from pathlib import Path
import subprocess
from datetime import datetime
from multiprocessing import Value
from utility import save_in_config

class Recorder():

    def __init__(self, second_recording_time: int, source: Path, directory: Path, filename: str, file_extension: str):
        self._second_recording_time : Value = Value('i',second_recording_time)
        self._source: Path = source
        self._directory: Path = directory
        self._filename: str = filename
        self._file_extension: str = file_extension

    def set_recording_time(self, second_recording_time: int) -> int:
        if int(second_recording_time) != self._second_recording_time.value:
            self._second_recording_time.value = int(second_recording_time)
            save_in_config('recording_time', int(second_recording_time))
        return self._second_recording_time.value

    def get_recording_time(self) -> int:
        return self._second_recording_time.value

    def _get_formatted_filename(self) -> str:
        filename = self._filename
        if "$" in filename:
            date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S").split("-")
            filename = filename.replace("$day",date[0])
            filename = filename.replace("$month",date[1])
            filename = filename.replace("$year",date[2])
            filename = filename.replace("$hour",date[3])
            filename = filename.replace("$min",date[4])
            filename = filename.replace("$sec",date[5])
        return filename

    def run_record(self) -> bool:
        raise NotImplementedError("Subclass must implement abstract method")

class SimpleVideoRecorder(Recorder):

    def __init__(self, second_recording_time: int, source: Path, directory: Path, filename: str, framerate: int, width: int, height: int):
        super().__init__(second_recording_time, source, directory, filename, "mpeg")
        self.__framerate = framerate
        self.__width = width
        self.__height = height

    def run_record(self) -> bool:
        subprocess.run(f"ffmpeg -f v4l2 -r {self.__framerate} -s {self.__width}x{self.__height} -t {self.get_recording_time()} -i {self._source} {self._directory}/{self._get_formatted_filename()}.{self._file_extension} -y", shell=True, check=True)
        
class VideoAudioRecorder(Recorder):

    def __init__(self, second_recording_time: int, source: Path, directory: Path, filename: str, framerate: int, width: int, height: int, sound_source: Path):
        super().__init__(second_recording_time, source, directory, filename, "mpeg")
        self.__framerate = framerate
        self.__width = width
        self.__height = height
        self.__sound_source = sound_source

    def run_record(self) -> bool:   
        subprocess.run(f"ffmpeg -f v4l2 -r {self.__framerate} -s {self.__width}x{self.__height} -i {self._source} -f alsa -i {self.__sound_source} -ac 2 -map 0:v -map 1:a -preset ultrafast -crf 14 -t {self.get_recording_time()} -y {self._directory}/{self._get_formatted_filename()}.{self._file_extension}", shell=True, check=True)