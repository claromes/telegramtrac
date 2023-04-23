import streamlit as st
from streamlit_extras.customize_running import center_running
import subprocess
import json
import configparser
from pandas import read_csv
import base64

#page config
st.set_page_config(
    page_title="telegramtrac",
    page_icon="👣",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://core.telegram.org/api/obtaining_api_id',
        'Report a bug': "https://github.com/claromes/telegramtrac",
        'About': """
        telegramtrac is Telegram public channels tracker for non-programmers by [claromes](https://claromes.gitlab.io).

        This project is a fork of DFRLab's Telegram Tracker.

        -------
        """
    }
)

#components variables
title_component = st.empty()
form_component = st.empty()
sign_in_component = st.empty()
channel_component = st.empty()
center_running()

trac = ''

#states
if 'channel_name' not in st.session_state:
    st.session_state['channel_name'] = 'literaturese'

if 'code_state' not in st.session_state:
    st.session_state['code_state'] = False

if 'code_value' not in st.session_state:
    st.session_state['code_value'] = 0

#title
title_component.title('telegramtrac', anchor=False)

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

if send_credentials and api_id != '' and api_hash != '' and phone != '':
    center_running()
    st.session_state.code_state = True

    # try:
    #     cmd_connect = 'python connect.py'

    #     output = subprocess.check_output(cmd_connect.split())
    # except subprocess.CalledProcessError as e:
    #     pass
    # except Exception as e:
    #     pass

#sign in code
with sign_in_component.form(key='config_sign_in_form'):
    if st.session_state.code_state:
        code_sign_in = st.text_input('code', disabled=False)
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
    if sign_in and not st.session_state.code_value == 0 or st.session_state.channel_name != '':
        channel_name = st.text_input('channel name', placeholder="https://t.me/CHANNEL_NAME_IS_HERE", disabled=False, key='channel_name')
        trac = st.form_submit_button('trac', disabled=False, type='primary')
        send_credentials = True
    else:
        channel_name = st.text_input('channel name', disabled=True)
        trac = st.form_submit_button('trac', disabled=True, type='primary')
        send_credentials = True

#data tabs
if trac and st.session_state.channel_name != '':
    center_running()
    tab1, tab2, tab3, tab4 = st.tabs(['json', 'dataset', 'metadata', 'new trac'])

    form_component.empty()
    sign_in_component.empty()
    channel_component.empty()

    # try:
    #     cmd_main = 'python main.py --telegram-channel {}'.format(st.session_state.channel_name)

    #     output = subprocess.check_output(cmd_main.split())
    # except subprocess.CalledProcessError as e:
    #     pass
    # except Exception as e:
    #     pass

    # try:
    #     cmd_dataset = 'python build-datasets.py'

    #     output = subprocess.check_output(cmd_dataset.split())
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
            st.download_button('{} Messages'.format(st.session_state.channel_name), help='Download {}_messages.json'.format(st.session_state.channel_name), file_name=json_file, data=file, mime='application/json')

            st.json(data, expanded=False)

    #dataset
    with tab2:
        st.subheader('{} dataset (.csv)'.format(st.session_state.channel_name))
        dataset_csv_file = 'output/data/msgs_dataset.csv'

        with open(dataset_csv_file, 'rb') as file:
            #st.download_button('Dataset', help='Download msgs_dataset.csv', file_name=dataset_csv_file, data=file, mime='text/csv')
            df = read_csv(dataset_csv_file)

            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()

            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="{dataset_csv_file}.csv" title="Download msgs_dataset.csv">Dataset</a>', unsafe_allow_html=True)

            st.dataframe(df)

    #metadata
    with tab3:
        metadata_json_file = 'output/data/{}/{}.json'.format(st.session_state.channel_name, st.session_state.channel_name)
        metadata_txt_file = 'output/data/chats.txt'
        metadata_chats_csv_file = 'output/data/collected_chats.csv'
        metadata_counter_csv_file = 'output/data/counter.csv'

        st.subheader('{} metadata'.format(st.session_state.channel_name))
        with open(metadata_json_file, 'rb') as file:
            st.download_button('{}'.format(st.session_state.channel_name), help='Download {}.json'.format(st.session_state.channel_name), file_name=metadata_json_file, data=file, mime="application/json")
        with open(metadata_txt_file, 'rb') as file:
            st.download_button('Chats', help='Download chats.txt', file_name=metadata_txt_file, data=file, mime='text/plain')
        with open(metadata_chats_csv_file, 'rb') as file:
            st.download_button('Collected Chats', help='Download collected_chats.csv', file_name=metadata_chats_csv_file, data=file, mime='text/csv')
        with open(metadata_counter_csv_file, 'rb') as file:
            st.download_button('Counter', help='Download counter.csv', file_name=metadata_counter_csv_file, data=file, mime='text/csv')

    #restart
    with tab4:
        restart = st.button('restart', type='primary')

        if restart:
            st.experimental_rerun()