# 🟦 telegramtrac

[![Bellingcat Accessibility Hackathon](https://img.shields.io/badge/%C2%BF%20Bellingcat%20Hackathon-April%202023-%23ffca8e?style=flat)](https://www.bellingcat.com/resources/2023/06/16/third-hackathon-open-source-tools/) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/claromes/telegramtrac?include_prereleases)](https://github.com/claromes/telegramtrac/releases)

A browser interface to Telegram’s API. Provides modules for connecting, signing in and communicating via Telethon. Generates files containing messages and metadata. It also includes additional modules for generating datasets and network graphs. telegramtrac is a [Telegram Tracker](https://github.com/estebanpdl/telegram-tracker) fork.

## Desktop (Serverless App)

> [!NOTE]
> The application can be resource-intensive, and the free Streamlit Cloud Community option is not sufficient. Therefore, I decided to compile telegramtrac to run locally. It is not necessary to configure any development environment; simply run the telegramtrac.exe file.

### Download

- Windows x64: [telegramtrac-0.6-installer-win-x64.zip]()

[Usage instructions](#usage)

### Built with

- Streamlit 1.25.0
- Nuitka 1.7.3 (standalone mode)
- Inno Setup 6.2.2

### Screenshots

<p align="center">
    <img src="images/splash-screen-telegram-0.6.png" height="260">
    <img src="assets/login.png" height="260">
</p>
<p align="center">
    <i>Splash screen (--onefile mode) and login</i>
</p>

<br>

<p align="center">
    <img src="assets/tracking.png" height="260">
    <img src="assets/messages.png" height="260">
</p>
<p align="center">
    <i>Tracking and messages visualization</i>
</p>

<br>

<p align="center">
    <img src="assets/dataset.png" height="260">
    <img src="assets/new_trac.png" height="260">
</p>
<p align="center">
    <i>Dataset visualization and new tracking/logoff</i>
</p>

<br>

<p align="center">
    <img src="assets/cmd.png" height="260">
</p>
<p align="center">
    <i>log (OS console/prompt)</i>
</p>

## Cloud

[![Test in Streamlit](https://img.shields.io/badge/Test%20in%20Cloud-fc7a7a?logo=streamlit&labelColor=eb4949&&logoColor=white)](https://telegramtrac.streamlit.app/)

The application is also available on [Streamlit Community Cloud](https://telegramtrac.streamlit.app) with limited server resources.

## Usage

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

### Folder structure

<details><summary><code>./config</code></summary>

    Telegram API credentials file (.ini)

</details>
<details><summary><code>./output_API_ID</code></summary>

    Telegram channel files (.json, .csv, .xlsx, .txt)

</details>
<details><summary><code>./session</code></summary>

    Telegram API session files (.session and .session-journal)

</details>
<details><summary><code>./sign_in</code></summary>

    Telegram API code and password encrypted files (.bin)

</details>
<details><summary><code>telegramtrac.exe</code></summary>

    telegramtrac's executable file

</details>

## Additional Information

### Limitations

- Only one channel per tracking

### Design decisions

Mostly limited to Streamlit options

## Development

### Requirements

- Operating System: Windows 64 bits
- Python 3.8+
- C Compiler
    - MSVC 14.3 (`--onefile mode`)
- Make (optional)

### Installation

$ `git clone git@github.com:claromes/telegramtrac.git`

$ `cd telegramtrac`

$ `pip install -r requirements.txt`

### Cloud version

$ `streamlit run app.py`

Streamlit will be served at http://localhost:8502

### Desktop version

$ `python telegramtrac.py`

The Streamlit main file is `app.py`.

Streamlit will be served at http://localhost:8502

### Build with Nuitka (Python compiler)

- --onefile mode

    $ `make onefile`

- --standalone mode

    $ `make standalone`

- non-distributable executable mode

    >[!NOTE]
    >To use the target `dev`, change `app_path` variable in telegramtrac.py file to `app_path_dev`

    $ `make dev`

Reference:
- [Nuitka User Manual](https://nuitka.net/doc/user-manual.html)

### Installer configuration with Inno Setup

References:

- [Inno Setup Documentation](https://jrsoftware.org/ishelp.php)
- [blog.pythonlibrary.org](https://www.blog.pythonlibrary.org/2019/03/19/distributing-a-wxpython-application/) (topic: Creating an Installer with Inno Setup)

## Bugs

- Desktop
    - [ ] Warnings:
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
- [x] Executable file
- [x] Add message about output folder (Desktop)
- [x] Keep *output_api_id* folder (Desktop)
- [x] Metadata files with channel name
- [x] Makefile to build/test
- [x] Serverless App without Python installed
- [x] Set up installer
- [ ] Set `Download` dir as output dir
- [ ] Encrypt config file
- [ ] Check login
- [ ] Multiples channels
- [ ] Network tab
- [x] Submit typing Enter
- [ ] Delete `subprocess.check_output`/ Update dir structure
    - [ ] Use `trio` instead of `asyncIO`
- [x] Splash screen (C compiler issue)
- [ ] Loading process explicit
- [ ] `DtypeWarning` (dataset)
- [ ] Check API limitations (FloodWaitError)
- [ ] Error msgs
    - [ ] FloodWaitError
    - [ ] Wrong password
    - [ ] Channel not found
- [ ] Build for Debian/Ubuntu/Mint
- [ ] Logout users (via Telethon)
- [ ] Option without API credentials

## [Changelog](/CHANGELOG.md)
