from Recorder import SimpleVideoRecorder
from Detector import AudioDetector
from pathlib import Path
import utility

def main():
    record_path = Path("./videos")
    simpleVideoRecorder = SimpleVideoRecorder(5, utility.get_logitech_4k_video_path(), record_path, "record_$day-$month-$year_$hour-$min-$sec", 25, 1920, 1080)
    audioDetector = AudioDetector(simpleVideoRecorder.run_record, utility.get_logitech_720p_mic_id())
    audioDetector.set_detection_threshold(1)
    audioDetector.start_detection()

    utility.run_file_web_werver(record_path)

if __name__ == '__main__':
    main()