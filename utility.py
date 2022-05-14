import pyaudio
import contextlib
import subprocess
from pathlib import Path
import re

def get_logitech_720p_mic_id() -> int:
    p = pyaudio.PyAudio()
    for mic_id in range(p.get_device_count()):
        if "USB Device 0x46d:0x825" in p.get_device_info_by_index(mic_id).get('name'):
            return mic_id
    return None

def get_mic_adapter_id() -> int:
    p = pyaudio.PyAudio()
    for mic_id in range(p.get_device_count()):
        if "C-Media USB Headphone Set" in p.get_device_info_by_index(mic_id).get('name'):
            return mic_id
    return None

def get_logitech_4k_mic_path() -> Path:
    p = pyaudio.PyAudio()
    for mic_id in range(p.get_device_count()):
        name = p.get_device_info_by_index(mic_id).get('name')
        if "Logitech BRIO: USB Audio" in name:
            return Path(name.split("(")[1][:-1])
    return None

def get_logitech_4k_video_path() -> Path:
    regex = r"Logitech BRIO.*\n *(.*)"
    try:
        match = re.search(regex, subprocess.check_output(['v4l2-ctl', '--list-devices']).decode("utf-8"), re.MULTILINE)
    except:
        print("Not found Logitech BRIO camera !")
        exit(1)
    return Path("".join(match.groups()[0].split()))

def test_detector():
    print("bip")