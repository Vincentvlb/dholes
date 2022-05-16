from Recorder import SimpleVideoRecorder, VideoAudioRecorder
from Detector import AudioDetector
from web_server import webserver
from pathlib import Path
import utility

def main():
    record_path = Path("./videos")
    detection_threshold = utility.get_in_config("detection_threshold", 95)
    recording_time = utility.get_in_config("recording_time", 30)
    #simpleVideoRecorder = SimpleVideoRecorder(5, utility.get_logitech_4k_video_path(), record_path, "record_$day-$month-$year_$hour-$min-$sec", 25, 1920, 1080)
    videoAudioRecorder = VideoAudioRecorder(recording_time, utility.get_logitech_4k_video_path(), record_path, "record_$day-$month-$year_$hour-$min-$sec", 20, 1920, 1080, utility.get_logitech_4k_mic_path())
    audioDetector = AudioDetector(videoAudioRecorder.run_record, utility.get_mic_adapter_id())
    audioDetector.set_threshold(detection_threshold)
    audioDetector.start_detection()

    server =  webserver.WebServer('./web_server', record_path, audioDetector.get_formatted_threshold, audioDetector.set_threshold, videoAudioRecorder.get_recording_time, videoAudioRecorder.set_recording_time)
    server.run_server("0.0.0.0", 80)

if __name__ == '__main__':
    main()