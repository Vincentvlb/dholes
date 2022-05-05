from Recorder import SimpleVideoRecorder
from Detector import AudioDetector
from web_server import webserver
from pathlib import Path
import utility

def main():
    record_path = Path("./videos")
    simpleVideoRecorder = SimpleVideoRecorder(5, utility.get_logitech_4k_video_path(), record_path, "record_$day-$month-$year_$hour-$min-$sec", 25, 1920, 1080)
    audioDetector = AudioDetector(simpleVideoRecorder.run_record, utility.get_logitech_720p_mic_id())
    audioDetector.set_threshold(10)
    audioDetector.start_detection()

    server =  webserver.WebServer('./web_server', record_path, audioDetector.get_formatted_threshold, audioDetector.set_threshold)
    server.run_server("0.0.0.0", 80)

if __name__ == '__main__':
    main()