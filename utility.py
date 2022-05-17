import pyaudio
import contextlib
import subprocess
from pathlib import Path
import re
import json
import os
import shutil
import time
import RPi.GPIO as GPIO

def setup_led():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    led_off("Blue")
    led_off("Green")

def led_on(color: str):
    if color == "Blue":
        GPIO.output(20, False)
    elif color == "Green":
        GPIO.output(21, False)

def led_off(color: str):
    if color == "Blue":
        GPIO.output(20, True)
    elif color == "Green":
        GPIO.output(21, True) 

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
    led_on("Blue")
    while(True):
        try:
            match = re.search(regex, subprocess.check_output(['v4l2-ctl', '--list-devices']).decode("utf-8"), re.MULTILINE)
            break
        except:
            print("Not found Logitech BRIO camera ! Retry in 10 sec...")
            time.sleep(10)
    led_off("Blue")
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

def add_service():
    if not os.path.isfile('/etc/systemd/system/dholes.service'):
        with open('dholes.service', 'w+') as file:
            file.write(f"[Unit]\nDescription=stream\nAfter=network.target\n \
            \n[Service]\nType=simple\nUser=root\nWorkingDirectory={os.getcwd()}/\nExecStart=/usr/bin/python3 {os.getcwd()}/main.py\nRestart=on-failure\n\
            \n[Install]\nWantedBy=multi-user.target")
        shutil.copyfile(f"dholes.service", f"/etc/systemd/system/dholes.service")
        os.system(f"sudo systemctl enable dholes.service")