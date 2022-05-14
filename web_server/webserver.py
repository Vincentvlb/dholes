from flask import Flask, render_template, send_from_directory, request, jsonify
import multiprocessing
import logging
import os
from glob import glob
from typing import Callable

class WebServer:

    def __init__(self, server_dir: str, upload_folder: str, get_threshold_callable: Callable, set_threshold_callable: Callable, get_recording_time_callable: Callable, set_recording_time_callable: Callable):
        self.__upload_folder = upload_folder
        self.__get_threshold_callable = get_threshold_callable
        self.__set_threshold_callable = set_threshold_callable
        self.__get_recording_time_callable = get_recording_time_callable
        self.__set_recording_time_callable = set_recording_time_callable
        self.__app = Flask("webserver", template_folder=os.path.abspath(server_dir+"/templates"), static_folder=os.path.abspath(server_dir+"/static"))

        self.__app.add_url_rule('/', view_func=self.__index)
        self.__app.add_url_rule('/videos/<filename>', view_func=self.__videos)
        self.__app.add_url_rule('/remove_file', view_func=self.__remove_file, methods=["POST"])
        self.__app.add_url_rule('/set_threshold', view_func=self.__set_threshold, methods=["POST"])
        self.__app.add_url_rule('/set_recording_time', view_func=self.__set_recording_time, methods=["POST"])
        
        """logging.getLogger('werkzeug').disabled = True
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'"""

    def run_server(self, host: str, port: int):
        self.__webStream = multiprocessing.Process(target=self.__app.run, args=(host, port, False))
        self.__webStream.start()

    def __index(self):
        files = glob(f"{self.__upload_folder}/*.mpeg")
        files.sort(key=os.path.getmtime)
        files.reverse()
        return render_template("index.html", files=files, threshold=self.__get_threshold_callable(), recording_time=self.__get_recording_time_callable())

    def __set_threshold(self):
        threshold = request.form.get("threshold")
        new_threshold = self.__set_threshold_callable(float(threshold))
        return jsonify(threshold=new_threshold)

    def __set_recording_time(self):
        recording_time = request.form.get("recording_time")
        new_recording_time = self.__set_recording_time_callable(float(recording_time))
        return jsonify(recording_time=new_recording_time)

    def __videos(self, filename):
        return send_from_directory(directory=self.__upload_folder, path=filename)

    def __remove_file(self):
        filename = request.form.get("filename")
        if os.path.exists(f"videos/{filename}"):
            os.remove(f"videos/{filename}")
            return jsonify(True)
        else:
            return jsonify(False)