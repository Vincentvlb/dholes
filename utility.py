import pyaudio
import contextlib
import subprocess
from pathlib import Path
import re

def get_logitech_720p_mic_id() -> int:
    p = pyaudio.PyAudio()
    for mic_id in range(p.get_device_count()):
        if p.get_device_info_by_index(mic_id).get('name') == "USB Device 0x46d:0x825: Audio (hw:2,0)":
            return mic_id
    return None

def get_logitech_4k_video_path() -> Path:
    regex = r"Logitech BRIO.*\n *(.*)"
    try:
        match = re.search(regex, subprocess.check_output(['v4l2-ctl', '--list-devices']).decode("utf-8"), re.MULTILINE)
    except:
        print("Not found Logitech BRIO camera !")
        exit(1)
    return Path("".join(match.groups()[0].split()))

def run_file_web_werver(record_path: Path) -> subprocess.Popen:
    return subprocess.Popen(["python3", "-m", "http.server"], cwd=record_path)

def test_detector():
    print("bip")