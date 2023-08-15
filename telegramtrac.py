# -*- coding: utf-8 -*-

'''
Copyright (c) Clarissa R Mendes (claromes) (2023)

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
import subprocess
import psutil
import sys
import tempfile
import os
import signal
import datetime
import webbrowser
from rich.console import Console
from rich import print

# --onefile mode
# if 'NUITKA_ONEFILE_PARENT' in os.environ:
#    splash_filename = os.path.join(
#       tempfile.gettempdir(),
#       'onefile_%d_splash_feedback.tmp' % int(os.environ['NUITKA_ONEFILE_PARENT']),
#    )

#    if os.path.exists(splash_filename):
#       os.unlink(splash_filename)

c = Console()

def run_app():
    cache_dir = os.environ.get('LOCALAPPDATA', '')
    # app_path = '{}\\Programs\\telegramtrac\\0.6.0.0-0.1.0.0\\app.py'.format(cache_dir) # --onefile mode
    app_path = '{}\\Programs\\telegramtrac\\app.py'.format(cache_dir)
    app_path_dev = 'app.py' # non-distributable executable mode

    sys.argv = [
        # '0', 'run', app_path,
        '0', 'run', app_path_dev,
        '--theme.base=dark',
        '--theme.primaryColor=rgb(46, 154, 255)',
        '--theme.backgroundColor=rgb(25, 25, 30)',
        '--theme.textColor=rgb(250, 250, 250)',
        '--theme.font=monospace',
        '--client.toolbarMode=minimal',
        '--global.developmentMode=false',
        '--server.port=8502',
        '--server.headless=true',
    ]

    name = 'main'
    year = datetime.datetime.now().year

    c.rule('telegramtrac', style='rgb(46,154,255)')
    c.print("\nA browser interface to Telegram's API", justify='left', style='rgb(165,165,165)')
    c.print('[rgb(165,165,165)]release v0.6[/]', justify='left')
    c.print('[rgb(165,165,165)]license Apache-2.0[/]', justify='left')

    c.print('\n[rgb(165,165,165)]Copyright © {} claromes[/]\n'.format(year), justify='left')

    c.rule('\nStreamlit log\n', style='rgb(255,75,75)')

    webbrowser.open('http://localhost:8502')
    stcli.main()

def on_closing():
    c.rule('\nStreamlit log\n', style='rgb(255,75,75)')

    for proc in psutil.process_iter(['pid', 'name']):
        for conn in proc.connections():
            if conn.laddr.port == 8502:
                pid = proc.info['pid']

    if pid:
        try:
            process = psutil.Process(pid)
            process.terminate()
            c.log('Process {} terminated successfully.'.format(pid), justify='left')
        except psutil.NoSuchProcess:
            c.log('Process {} not found.'.format(pid), justify='left')
        except psutil.AccessDenied:
            c.log('Permission denied to terminate process {}.'.format(pid), justify='left')

def signal_handler(signum, frame):
    on_closing()

    app_process.terminate()
    app_process.join()

    exit(0)

if __name__ == '__main__':
    app_process = multiprocessing.Process(target=run_app)

    signal.signal(signal.SIGINT, signal_handler)

    app_process.start()
    app_process.join()
