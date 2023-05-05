# telegramtrac

![GitHub release (latest by date)](https://img.shields.io/github/v/release/claromes/telegramtrac)

## Team Members
[claromes](https://claromes.gitlab.io/)

## Tool Description
telegramtrac is a web-based tool designed for tracking public channels on Telegram. It's a fork of the package [`telegram-tracker`](https://github.com/estebanpdl/telegram-tracker) developed by Esteban Ponce de León, DFRLab researcher.

I became familiar with the package during the DFRLab's Digital Sherlocks Program and believe that an accessible version would benefit researchers of different skill levels.

## Requirements

- Python 3.8+

## Installation

$ `git clone git@github.com:claromes/telegramtrac.git`

$ `cd telegramtrac`

$ `pip install -r requirements.txt`

$ `streamlit run streamlit/telegramtrac.py`

Streamlit will be served at http://localhost:8501

## Usage

### Browser interface

<br>
<p align="center">
    <img src="assets/1.png" width="700">
</p>

### Workflow

1. Create your API credentials [here](https://my.telegram.org/auth)

<p align="center">
    <img src="assets/2.png" width="400">
</p>
<p align="center">
    <img src="assets/3.png" width="400">
</p>

2. Fill the inputs `api_id`, `api_hash` and your `phone` number (*following this format: +5500912348765*) and click on `send credentials` button

- A 5-digit code will be send to your Telegram app

3. Fill the input `code` and `password` (For Two-Step Verification enabled users) and click on `sign in` button

- A message will be send to your Telegram app about the authentication

4. Fill the input `channel name` (*copy name from channel link: t.me/CHANNEL_NAME*) and click on `trac` button

- It may take a few minutes...

5. Switch tabs to preview or download the data

6. To track another channel, switch to last tab (`trac`) and click `new trac`.

7. Fill the input `channel name` (*copy name from channel link: t.me/CHANNEL_NAME*) and click on `trac` button

- At each tracking the dataset are grouped in the same file to allow network analysis

## Additional Information

### Limitations

- Only one channel per track
- Each sign-in generates a new instance

### Design decisions

Mostly limited to Streamlit options. The form and tabs were chosen due to common use in web apps.

## Roadmap

- [x] Fix dataset tab
- [x] Fix set credentials and code in restart flow
- [x] Allow 2FA
- [ ] One session/sign_in file per user
- [ ] sqlite3.OperationalError
- [ ] Tabs description
- [ ] Add batch file upload
- [ ] Option without API credentials
- [ ] Network tab
- [ ] Delete `subprocess.check_output`/ Update dir structure
- [ ] Logout users (with Telethon)
- [ ] FloodWaitError msg
- [x] Error msgs
- [ ] Storage limit alerts
- [x] Delete files after session finish
- [ ] Log for users
- [ ] Docs telegramtrac/ API credentials (how to)
- [ ] Check API limitations
- [ ] Sec issues

## Changelog

- [v0.4.0](https://github.com/claromes/telegramtrac/releases/tag/v0.4.0)
    - Allow 2FA
    - Store encrypted code and password
    - Add log out button
    - Delete *.session and *.bin files
- [v0.3.1](https://github.com/claromes/telegramtrac/releases/tag/v0.3.1)
    - Each sign-in generates a new instance
    - Add sidebar
    - Add general error messages
- [v0.3.0](https://github.com/claromes/telegramtrac/releases/tag/v0.3.0)
    - Fix new tracking flow
    - Delete output dir
- [v0.2.0](https://github.com/claromes/telegramtrac/releases/tag/v0.2.0)
    - Fix dataset tab
    - Fix imports
- [v0.1.0](https://github.com/claromes/telegramtrac/releases/tag/v0.1.0)
    - Bellingcat Accessibility Hackathon submission
