# 🟦 telegramtrac

[![Bellingcat Accessibility Hackathon](https://img.shields.io/badge/%C2%BF%20Bellingcat%20Hackathon-April%202023-%23ffca8e?style=flat)](https://www.bellingcat.com/resources/2023/06/16/third-hackathon-open-source-tools/) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/claromes/telegramtrac?include_prereleases)](https://github.com/claromes/telegramtrac/releases)

A browser interface to Telegram’s API. Provides modules for connecting, signing in and communicating via Telethon. Generates files containing messages and metadata. It also includes additional modules for data analysis. telegramtrac is a [Telegram Tracker](https://github.com/estebanpdl/telegram-tracker) fork.

## Cloud App

> [!NOTE]
> The application can be resource-intensive, and the free Streamlit Cloud Community option is not sufficient. Therefore, setting up the development environment and running locally may be more effective for Telegram channels with a lot of activity.

[![Open in Streamlit](https://img.shields.io/badge/Test%20in%20Cloud-fc7a7a?logo=streamlit&labelColor=eb4949&&logoColor=white)](https://telegramtrac.streamlit.app/)

The application is available on [Streamlit Community Cloud](https://telegramtrac.streamlit.app) with limited server resources.

## Usage

1. Create your API credentials [here](https://my.telegram.org/auth)

<p align="center">
    <img src="assets/credentials_1.png" width="350">
    <img src="assets/credentials_2.png" width="350">
</p>
<p align="center">

</p>

2. Enter the input `api_id`, `api_hash` and `phone` (e.g., +55912348765), then click on the `send credentials` button

- A 5-digit code will be send to your Telegram app

3. Enter the input `code` and `password` (optional), then click on the `sign in` button

- A confirmation message will be send to your Telegram app

4. Enter the input `channel name` (*t.me/CHANNEL_NAME_IS_HERE*), then click on the `trac` button

- It may take a few minutes...

5. Switch tabs to preview or download the data

6. To tracking another channel, switch to the last tab (`trac`) and click `new trac`.

    6.1. Enter the input `channel name` (*t.me/CHANNEL_NAME_IS_HERE*), then click on the `trac` button

7. To finish and delete all credentials/session files, click on the `log out` button

- At each tracking the dataset are grouped in the same file to allow network analysis

## Additional Information

### Limitations

- Only one channel per tracking

### Design decisions

Mostly limited to Streamlit options

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
        - Do not displays requested data and instead  "new trac" component
    - [ ] `requirements.txt` installation on Streamlit Cloud

## Docs

- [Roadmap](docs/ROADMAP.md)
- [Changelog](docs/CHANGELOG.md)
