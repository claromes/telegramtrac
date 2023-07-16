# telegramtrac

[![Bellingcat Accessibility Hackathon](https://img.shields.io/badge/%C2%BF%20Bellingcat%20Hackathon-April%202023-%23ffca8e?style=flat)](https://www.bellingcat.com/resources/2023/06/16/third-hackathon-open-source-tools/) [![Test in Streamlit](https://img.shields.io/badge/Test%20in%20Streamlit-fc7a7a?logo=streamlit&labelColor=eb4949&&logoColor=white)](https://telegramtrac.streamlit.app/) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/claromes/telegramtrac)](https://github.com/claromes/telegramtrac/releases) (not stable)

A browser interface to Telegram’s API. Provides modules for connecting, signing in and communicating via Telethon. Generates files containing messages and metadata. It also includes additional modules for generating datasets and network graphs.

It's a fork of [Telegram Tracker](https://github.com/estebanpdl/telegram-tracker).

## Desktop (Serverless App)

*The application can be resource-intensive, and the free Streamlit Cloud Community option is not sufficient. Therefore, I decided to compile telegramtrac to run locally. It is not necessary to configure any development environment; simply run the telegramtrac.exe file.*

- Windows 10: [telegramtrac 0.6-beta.zip]()

Extract the contents of the ZIP folder to access the bundled content, and then run it.

Console/Command Prompt is enable to provide logs.

### Folder structure

<details><summary><code>./</code></summary>

    python packages (*.pyd)
    libs (*.dll)

</details>
<details><summary><code>.streamlit</code></summary>

    Streamlit configurations

</details>
<details><summary><code>/config</code></summary>

    Telegram API credentials files (*.ini)

</details>
<details><summary><code>/session</code></summary>

    Telegram API sessions files (*.session and *.session-journal)

</details>
<details><summary><code>/sign_in</code></summary>

    Telegram API code and password encrypted files (*.bin)

</details>
<details><summary><code>/telegram-tracker</code></summary>

    Telegram Tracker package code

</details>
<details><summary><code>app.py</code></summary>

    Streamlit app

</details>
<details><summary><code>build-datasets.py</code></summary>

    Creates a new dataset containing messages from the requested channels

</details>
<details><summary><code>channels-to-network.py</code></summary>

    Builds a network graph

</details>
<details><summary><code>connect.py</code></summary>

    Connecting module to the Telegram API

</details>
<details><summary><code>main.py</code></summary>

    Main file of Telegram Tracker package

</details>
<details><summary><code>sign_in.py</code></summary>

    Signing module to the Telegram API

</details>
<details><summary><code>telegramtrac.exe</code></summary>

    telegramtrac's executable file

</details>
<details><summary><code>telegramtrac.py</code></summary>

    Webview and Streamlit processes. telegramtrac main file

</details>

## Cloud

The application is also available on [Streamlit Community Cloud](https://telegramtrac.streamlit.app) with limited server resources.

## Development

### Requirement

- Python 3.8+

### Installation

$ `git clone git@github.com:claromes/telegramtrac.git`

$ `cd telegramtrac`

$ `pip install -r requirements.txt`

$ `streamlit run app.py`

Streamlit will be served at http://localhost:8502

### Build with Nuitka (Python compiler)

$ `python -m nuitka --standalone --remove-output --output-dir=output --include-package=typing_extensions --windows-icon-from-ico=icon/icon.ico telegramtrac.py`

*To test locally delete the `--standalone` option*

## Usage

### Browser interface

<br>
<p align="center">
    <img src="assets/interface.png" width="700">
</p>

### Workflow

1. Create your API credentials [here](https://my.telegram.org/auth)

<p align="center">
    <img src="assets/credentials_1.png" width="400">
</p>
<p align="center">
    <img src="assets/credentials_2.png" width="400">
</p>

2. Enter the input `api_id`, `api_hash` and `phone` (e.g., +55912348765), then click on the `send credentials` button

- A 5-digit code will be send to your Telegram app

3. Enter the input `code` and `password` (optional), then click on the `sign in` button

- A confirmation message will be send to your Telegram app

4. Enter the input `channel name` (*t.me/CHANNEL_NAME_IS_HERE*), then click on the `trac` button

- It may take a few minutes...

5. Switch tabs to preview or download the data

6. To tracking another channel, switch to last tab (`trac`) and click `new trac`.

    6.1. Enter the input `channel name` (*t.me/CHANNEL_NAME_IS_HERE*), then click on the `trac` button

7. To finish and delete all credentials/session/code/password, click on the `log out` button

- At each tracking the dataset are grouped in the same file to allow network analysis

## Additional Information

### Limitations

- Only one channel per tracking

### Design decisions

Mostly limited to Streamlit options.

## Bugs

- Desktop
    - [ ] Warnings:
        - Missing WebView2Loader.dll
        - UserWarning: loaded more than 1 DLL from .libs
    - [x] Close console

- Streamlit Cloud
    - [ ] "sqlite3.OperationalError: database is locked" issue on long-running requests
        - Do not displays requested data and instead  "new trac" component
    - [ ] `requirements.txt` installation on Streamlit Cloud

## Roadmap

- [x] Fix dataset tab
- [x] Fix set credentials and code in restart flow
- [x] Allow 2FA
- [x] One session/sign_in file per user
- [x] Generic error msgs
- [x] Delete files after session finish
- [x] Add download
    - [x] `collected_chats.xlsx`
    - [x] `user_exceptions.txt`
- [x] Desktop bundle (v0.6)
- [ ] Locate data files (v0.6)
- [ ] Submit typing Enter (v0.6)
- [ ] GitHub Actions
- [ ] Metadata files with channel name (v0.6.1)
- [ ] Encrypt config file (v0.6.2)
- [ ] Multiples channels (v0.6.2)
- [ ] Network tab (v0.6.3)
- [ ] Delete `subprocess.check_output`/ Update dir structure
    - [ ] Use `trio` instead of `asyncIO`
- [ ] Loading process explicit
- [ ] `DtypeWarning` (dataset)
- [ ] Logout users (via Telethon)
- [ ] Check API limitations (FloodWaitError)
- [ ] Error msgs
    - [ ] FloodWaitError
    - [ ] Channel not found
- [ ] Option without API credentials
- [ ] Build for Debian/Ubuntu/Mint

## [Changelog](/CHANGELOG.md)
