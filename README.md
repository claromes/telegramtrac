# telegramtrac

![Bellingcat Accessibility Hackathon](https://img.shields.io/badge/%C2%BF%20Bellingcat%20Hackathon-April%202023-%23ffca8e?style=flat) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_red.svg)](https://telegramtrac.streamlit.app/) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/claromes/telegramtrac)](https://github.com/claromes/telegramtrac/releases) (not stable)

A web-based tool designed for tracking public channels on Telegram. Provides modules for connecting, signing in and communicating with Telegram API via Telethon. It also includes additional modules for generating datasets and network graphs.

It's a fork of [`telegram-tracker`](https://github.com/estebanpdl/telegram-tracker) developed by Esteban Ponce de León (DFRLab).

## Requirements

- Python 3.8+

## Installation

$ `git clone git@github.com:claromes/telegramtrac.git`

$ `cd telegramtrac`

$ `pip install -r requirements.txt`

$ `streamlit run app.py`

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

### Design decisions

Mostly limited to Streamlit options. The form and tabs were chosen due to common use in web apps.

## Roadmap

[ROADMAP.md](/ROADMAP.md)

## Changelog

[CHANGELOG.md](/CHANGELOG.md)
