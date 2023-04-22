import streamlit as st
from streamlit_extras.customize_running import center_running
import subprocess
import json
import configparser
from pandas import read_csv

#vars
title_component = st.empty()
expander_component = st.empty()
form_component = st.empty()
sign_in_component = st.empty()
channel_component = st.empty()
center_running()

trac = ''

if 'channel_name' not in st.session_state:
    st.session_state['channel_name'] = 'literaturese'

if 'code_state' not in st.session_state:
    st.session_state['code_state'] = False

if 'code_value' not in st.session_state:
    st.session_state['code_value'] = 0

#title
title_component.title('telegramtrac')

#expander
with expander_component.expander('[ ¿ ]'):
    st.caption("Telegram channel tracker for non-programmers.")
    st.divider()
    st.caption('### How to')
    st.caption('[How to create an API ID and API hash](https://core.telegram.org/api/obtaining_api_id)')
    st.divider()
    st.caption('### Credits')
    st.caption("telegramtrac by [claromes](https://claromes.gitlab.io) is a fork of DFRLab's Telegram Tracker.")

#credentials
with form_component.form(key='config_form'):
    ***REMOVED*** st.text_input('api_id')
    ***REMOVED*** st.text_input('api_hash')
    ***REMOVED*** st.text_input('phone')

    config = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone': phone
    }

    config_parser = configparser.ConfigParser()
    config_parser['Telegram API credentials'] = config
    with open('config/config.ini', 'w') as file:
        config_parser.write(file)

    send_credentials = st.form_submit_button('send credentials', type='primary')

if send_credentials:
    center_running()
    st.session_state.code_state = True

#sign in code
with sign_in_component.form(key='config_sign_in_form'):
    if st.session_state.code_state:
        code_sign_in = st.text_input('code', placeholder="Leave empty and click 'sign in' to receive a sign in code", disabled=False)
    else:
        code_sign_in = st.text_input('code', disabled=True)

    if code_sign_in == '':
        code_sign_in = st.session_state.code_value

    config_sign_in_***REMOVED*** {
        'code': code_sign_in
    }

    config_sign_in_code_parser = configparser.ConfigParser()
    config_sign_in_code_parser['Sign in code'] = config_sign_in_code
    with open('config/config_sign_in_code.ini', 'w') as file:
        config_sign_in_code_parser.write(file)

    if st.session_state.code_state:
        sign_in = st.form_submit_button('sign in', disabled=False, type='primary')
    else:
        sign_in = st.form_submit_button('sign in', disabled=True, type='primary')

    if sign_in:
        center_running()
        st.session_state.code_value = code_sign_in

#channel name
with channel_component.form(key='channel_form'):
    if sign_in and not st.session_state.code_value == 0:
        channel_name = st.text_input('channel name', placeholder="https://t.me/CHANNEL_NAME_IS_HERE", disabled=False, key='channel_name')
        trac = st.form_submit_button('trac', disabled=False, type='primary')
        send_credentials = True
    else:
        channel_name = st.text_input('channel name', disabled=True)
        trac = st.form_submit_button('trac', disabled=True, type='primary')
        send_credentials = True

#data tabs
if trac:
    center_running()
    tab1, tab2, tab3, tab4 = st.tabs(['json', 'dataset', 'metadata', 'new trac'])

    expander_component.empty()
    form_component.empty()
    sign_in_component.empty()
    channel_component.empty()

    #SEC ISSUE: New login message not being sent
    # try:
    #     cmd = 'python main.py --telegram-channel {}'.format(st.session_state.channel_name)

    #     output = subprocess.check_output(cmd.split())
    # except subprocess.CalledProcessError as e:
    #     pass
    # except Exception as e:
    #     pass

    #json - main file
    with tab1:
        json_file = 'output/data/{}/{}_messages.json'.format(st.session_state.channel_name, st.session_state.channel_name)
        with open(json_file, 'rb') as file:
            st.subheader('{} messages (.json)'.format(st.session_state.channel_name))

            data = json.load(file)
            st.download_button('Download {}_messages.json'.format(st.session_state.channel_name), file_name=json_file, data=file, mime="application/json")

            st.json(data)

    #dataset
    with tab2:
        st.subheader('{} dataset (.csv)'.format(st.session_state.channel_name))
        dataset_csv_file = 'output/data/msgs_dataset.csv'

        with open(dataset_csv_file, 'rb') as file:
            st.download_button("Download msgs_dataset.csv", file_name=dataset_csv_file, data=file, mime="text/csv")
            df = read_csv(dataset_csv_file)

            st.dataframe(df)

    #metadata
    with tab3:
        metadata_json_file = 'output/data/{}/{}.json'.format(st.session_state.channel_name, st.session_state.channel_name)
        metadata_txt_file = 'output/data/chats.txt'
        metadata_chats_csv_file = 'output/data/collected_chats.csv'
        metadata_counter_csv_file = 'output/data/counter.csv'

        st.subheader('{} metadata'.format(st.session_state.channel_name))
        with open(metadata_json_file, 'rb') as file:
            st.download_button('Download {}.json'.format(st.session_state.channel_name), file_name=metadata_json_file, data=file, mime="application/json")
        with open(metadata_txt_file, 'rb') as file:
            st.download_button("Download chats.txt", file_name=metadata_txt_file, data=file, mime="text/plain")
        with open(metadata_chats_csv_file, 'rb') as file:
            st.download_button("Download collected_chats.csv", file_name=metadata_chats_csv_file, data=file, mime="text/csv")
        with open(metadata_counter_csv_file, 'rb') as file:
            st.download_button("Download counter.csv", file_name=metadata_counter_csv_file, data=file, mime="text/csv")

    #restart
    with tab4:
        restart = st.button('restart', type='primary')

        if restart:
            st.experimental_rerun()