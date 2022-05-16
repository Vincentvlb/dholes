import pyaudio
import contextlib
import subprocess
from pathlib import Path
import re
import json
import os

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

def save_in_config(key: str, value):
    if not os.path.isfile('config.json'):
        with open('config.json', 'w+') as file:
            file.write("{}")
    with open('config.json', 'r+') as file:
        data = json.load(file)
        data[key] = value
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def load_config():
    if os.path.isfile('config.json'):
        with open('config.json', 'r') as file:
            data = json.load(file)
            return data
    else:
        return None

def get_in_config(key: str, default_value):
    config = load_config()
    if config is None or key not in config:
        return default_value
    return config[key]