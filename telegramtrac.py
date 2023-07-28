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
import tempfile
import os

if 'NUITKA_ONEFILE_PARENT' in os.environ:
   splash_filename = os.path.join(
      tempfile.gettempdir(),
      'onefile_%d_splash_feedback.tmp' % int(os.environ['NUITKA_ONEFILE_PARENT']),
   )

   if os.path.exists(splash_filename):
      os.unlink(splash_filename)

window = webview.create_window(title='telegramtrac', url='http://localhost:8502', width=1280, height=720, background_color='#19191E')

def run_webview():
    webview.start(private_mode=True, gui='edgechromium')

def run_app():
    cache_dir = os.environ.get('LOCALAPPDATA', '')
    app_path = '{}\\telegramtrac\\telegramtrac\\0.6.0.0-0.1.0.0\\app.py'.format(cache_dir)

    subprocess.Popen(['python', '-m', 'streamlit', 'run', 'app.py', '--global.developmentMode=false', '--server.port=8502', '--server.headless=true'])

def on_closing():
    print('Stopping...')

    for proc in psutil.process_iter(['pid', 'name']):
        for conn in proc.connections():
            if conn.laddr.port == 8502:
                pid = proc.info['pid']

    if pid:
        try:
            process = psutil.Process(pid)
            process.terminate()
            print('Process {} terminated successfully.'.format(pid))
        except psutil.NoSuchProcess:
            print('Process {} not found.'.format(pid))
        except psutil.AccessDenied:
            print('Permission denied to terminate process {}.'.format(pid))

window.events.closing += on_closing

app_process = multiprocessing.Process(target=run_app)
webview_process = multiprocessing.Process(target=run_webview)

if __name__ == '__main__':
    app_process.start()
    webview_process.start()

    app_process.join()
    webview_process.join()
