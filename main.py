from Recorder import SimpleVideoRecorder
from Detection import AudioDetector

def main():
    simpleVideoRecorder = SimpleVideoRecorder(2, Path("/dev/video0", Path("./videos"), 20, 1920, 1080))
    audioDetector = AudioDetector(simpleVideoRecorder.run_record)
    audioDetector.start_detection()

if __name__ == '__main__':
    main()