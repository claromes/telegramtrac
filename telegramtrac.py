# -*- coding: utf-8 -*-

'''
Copyright (c) Clarissa R Mendes (2023)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import streamlit.web.cli as stcli
import multiprocessing
import webview
import subprocess
import psutil
import sys
import ctypes
import time
import tempfile
import os

app_process_pid = None
webview_process_pid = None

time.sleep(2)

if "NUITKA_ONEFILE_PARENT" in os.environ:
   splash_filename = os.path.join(
      tempfile.gettempdir(),
      "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]),
   )

   if os.path.exists(splash_filename):
      os.unlink(splash_filename)

window = webview.create_window(title='telegramtrac', url='http://localhost:8502', width=1280, height=720, background_color='#19191E')
is_closed = False

def run_webview():
    webview.start(private_mode=True)

def run_app():
    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    print(app_path)

    if os.path.exists(app_path):
        streamlit.bootstrap.run(filename,'',args)
        subprocess.Popen(['streamlit', 'run', app_path])

def on_closed():
    global app_process_pid, webview_process_pid
    app_process_handle = psutil.Process(app_process_pid)
    webview_process_handle = psutil.Process(webview_process_pid)

    app_process_handle.terminate()
    webview_process_handle.terminate()

    webview_process.wait()
    app_process.wait()

    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleCtrlHandler(None, 1)
        ctypes.windll.kernel32.GenerateConsoleCtrlEvent(0, 0)
        ctypes.windll.kernel32.FreeConsole()

    sys.exit()

    window.events.closed += on_closed

if __name__ == '__main__':
    app_process = multiprocessing.Process(target=run_app)
    webview_process = multiprocessing.Process(target=run_webview)

    app_process_pid = app_process.pid
    webview_process_pid = webview_process.pid

    app_process.start()
    webview_process.start()
