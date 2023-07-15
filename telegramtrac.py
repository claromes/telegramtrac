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
