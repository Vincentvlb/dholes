from Recorder import SimpleVideoRecorder
from Detector import AudioDetector
from pathlib import Path
import utility

def main():
    simpleVideoRecorder = SimpleVideoRecorder(5, utility.get_logitech_4k_video_path(), Path("./videos"), "record", 25, 1920, 1080)
    audioDetector = AudioDetector(simpleVideoRecorder.run_record, utility.get_logitech_720p_mic_id())
    audioDetector.set_detection_threshold(2)
    audioDetector.start_detection()

if __name__ == '__main__':
    main()