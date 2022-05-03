from pathlib import Path
import subprocess

class Recorder():

    def __init__(self, second_recording_time: int, source: Path, directory: Path, filename: str, file_extension: str):
        self.__second_recording_time: int = recording_time
        self.__source: Path = source
        self.__directory: Path = directory
        self.__filename: str = filename
        self.__file_extension: str = file_extension

    def run_record(self) -> bool:
        raise NotImplementedError("Subclass must implement abstract method")

class SimpleVideoRecorder():

    def __init__(self, second_recording_time: int, source: Path, directory: Path, framerate, width, height):
        super().__init__(second_recording_time, source, directory)
        self.__framerate = framerate
        self.__width = width
        self.__height = height

    def run_record(self) -> bool:
        subprocess.run(f"ffmpeg -f v4l2 -r {self.__framerate} -s {self.__width}x{self.__height} -t {self.__second_recording_time} -i {self.__source} {self.__directory}/{self.__filename}.{self.__file_extension}", shell=True, check=True)
