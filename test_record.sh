ffmpeg -f v4l2 -r 30 -s 1920x1080 -t 5 -i /dev/video0 videos/recording.avi

ffmpeg -f v4l2 -r 25 -s 1920x1080 -i /dev/video0 -segment_time 3 -segment_wrap 5 -f segment videos/%03d.ts

