# 🟦 telegramtrac

[![Bellingcat Accessibility Hackathon](https://img.shields.io/badge/%C2%BF%20Bellingcat%20Hackathon-April%202023-%23ffca8e?style=flat)](https://www.bellingcat.com/resources/2023/06/16/third-hackathon-open-source-tools/) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_red.svg)](https://telegramtrac.streamlit.app/) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/claromes/telegramtrac?include_prereleases)](https://github.com/claromes/telegramtrac/releases)

A browser interface to Telegram’s API. Provides modules for connecting, signing in and communicating via Telethon. Generates files containing messages and metadata. It also includes additional modules for data analysis. telegramtrac is a fork of the Python package Telegram Tracker.

The application is available on Streamlit Community Cloud with limited server resources.

> [!NOTE]
> The application can be resource-intensive, and the free Streamlit Cloud Community option is not sufficient. Therefore, setting up the development environment and running locally may be more effective for Telegram channels with a lot of activity.

## Usage

1. Create your API credentials [here](https://my.telegram.org/auth)

2. Enter the input `api_id`, `api_hash` and `phone` (e.g., +55912348765), then click on the `send credentials` button

- A 5-digit code will be send to your Telegram app

3. Enter the input `code` and `password` (optional), then click on the `sign in` button

- A confirmation message will be send to your Telegram app

4. Enter the input `channels (semicolon separated)`, then click on the `trac` button

- It may take a few minutes...

5. Switch tabs to preview or download the data

7. To finish and delete all credentials/session files, click on the `delete session files` button

## Development

### Requirements

- Telegram API credentials
- Python 3.8+

### Installation

$ `git clone git@github.com:claromes/telegramtrac.git`

$ `cd telegramtrac`

$ `pip install -r requirements.txt`

$ `streamlit run app.py`

Streamlit will be served at http://localhost:8501

## Bugs

- Streamlit Cloud
    - [ ] "sqlite3.OperationalError: database is locked" issue on long-running requests
        - Do not displays requested data
    - [ ] `requirements.txt` installation on Streamlit Cloud

## Docs

- [Roadmap](docs/ROADMAP.md)
- [Changelog](docs/CHANGELOG.md)
