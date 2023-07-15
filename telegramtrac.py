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

window = webview.create_window(title='telegramtrac', url='http://localhost:8502', width=1280, height=720, background_color='#19191E')
is_closed = False

def run_webview():
    webview.start(private_mode=True)

def run_app():
    subprocess.Popen(['streamlit', 'run', 'app.py'])

def on_closed():
    global is_closed

    is_closed = True

window.events.closed += on_closed

if __name__ == '__main__':
    app_process = multiprocessing.Process(target=run_app)
    webview_process = multiprocessing.Process(target=run_webview)

    app_process_pid = app_process.pid
    webview_process_pid = webview_process.pid

    app_process.start()
    webview_process.start()

    if is_closed:
        app_process_handle = psutil.Process(app_process_pid)
        webview_process_handle = psutil.Process(webview_process_pid)

        app_process_handle.terminate()
        webview_process_handle.terminate()

        webview_process.wait()
        app_process.wait()

        sys.exit()
