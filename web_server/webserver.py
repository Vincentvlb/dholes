from flask import Flask, render_template, send_from_directory, request, jsonify
import multiprocessing
import logging
import os
from glob import glob
from typing import Callable

class WebServer:

    def __init__(self, server_dir: str, upload_folder: str, get_threshold: Callable, set_threshold: Callable):
        self.__upload_folder = upload_folder
        self.__get_threshold = get_threshold
        self.__set_threshold = set_threshold
        self.__app = Flask("webserver", template_folder=os.path.abspath(server_dir+"/templates"), static_folder=os.path.abspath(server_dir+"/static"))

        self.__app.add_url_rule('/', view_func=self.index)
        self.__app.add_url_rule('/videos/<filename>', view_func=self.videos)
        self.__app.add_url_rule('/set_threshold', view_func=self.set_threshold, methods=["POST"])
        
        """logging.getLogger('werkzeug').disabled = True
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'"""

    def run_server(self, host: str, port: int):
        self.__webStream = multiprocessing.Process(target=self.__app.run, args=(host, port, False))
        self.__webStream.start()

    def index(self):
        files = glob(f"{self.__upload_folder}/*.mpeg")
        files.sort(key=os.path.getmtime)
        files.reverse()
        return render_template("index.html", files=files, threshold=self.__get_threshold())

    def set_threshold(self):
        threshold = request.form.get("threshold")
        self.__set_threshold(float(threshold))
        return ('', 204)

    def videos(self, filename):
        return send_from_directory(directory=self.__upload_folder, path=filename)