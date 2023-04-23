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
    st.session_state['channel_name'] = ''

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

try:
    cmd_tele = 'pip install --upgrade telethon'

    output = subprocess.check_output(cmd_tele.split())

    cmd_pd = 'pip install --upgrade pandas'

    output = subprocess.check_output(cmd_pd.split())
except Exception:
    pass

if send_credentials and api_id != '' and api_hash != '' and phone != '':
    center_running()
    st.session_state.code_state = True

    try:
        # cmd_pip = 'pip install -r requirements.txt'

        # output = subprocess.check_output(cmd_pip.split())

        cmd_connect = 'python connect.py'

        output = subprocess.check_output(cmd_connect.split())
    except subprocess.CalledProcessError:
        pass
    except Exception:
        pass

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

    try:
        cmd_main = 'python main.py --telegram-channel {}'.format(st.session_state.channel_name)

        output = subprocess.check_output(cmd_main.split())
    except subprocess.CalledProcessError:
        pass
    except Exception:
        pass

    try:
        cmd_dataset = 'python build-datasets.py'

        output = subprocess.check_output(cmd_dataset.split())
    except subprocess.CalledProcessError:
        pass
    except Exception:
        pass

    #json - main file
    with tab1:
        json_file = 'output/data/{}/{}_messages.json'.format(st.session_state.channel_name, st.session_state.channel_name)

        with open(json_file, 'rb') as file:
            st.subheader('{} messages (.json)'.format(st.session_state.channel_name))

            data = json.load(file)
            json_dump = json.dumps(data)
            b64 = base64.b64encode(json_dump.encode()).decode()
            href = 'data:file/json;base64,{}'.format(b64)

            st.markdown('<a href="{}" download="{}_messages.json" title="Download {}_messages.json">{} Messages</a>'.format(href, st.session_state.channel_name, st.session_state.channel_name, st.session_state.channel_name), unsafe_allow_html=True)
            st.json(data, expanded=False)

    #metadata
    with tab2:
        metadata_json_file = 'output/data/{}/{}.json'.format(st.session_state.channel_name, st.session_state.channel_name)
        metadata_txt_file = 'output/data/chats.txt'
        metadata_chats_csv_file = 'output/data/collected_chats.csv'
        metadata_counter_csv_file = 'output/data/counter.csv'

        st.subheader('{} metadata'.format(st.session_state.channel_name))
        with open(metadata_json_file, 'rb') as file:
            data = json.load(file)
            json_dump = json.dumps(data)

            b64 = base64.b64encode(json_dump.encode()).decode()
            href = 'data:file/json;base64,{}'.format(b64)

            st.markdown('<a href="{}" download="{}.json" title="Download {}.json">{}</a>'.format(href, st.session_state.channel_name, st.session_state.channel_name, st.session_state.channel_name), unsafe_allow_html=True)

        with open(metadata_txt_file, 'rb') as file:
            txt = file.read().decode()

            b64 = base64.b64encode(txt.encode()).decode()
            href = 'data:file/txt;base64,{}'.format(b64)

            st.markdown('<a href="{}" download="chats.txt" title="Download chats.txt">Chats</a>'.format(href), unsafe_allow_html=True)

        with open(metadata_chats_csv_file, 'rb') as file:
            metadata_chats = read_csv(metadata_chats_csv_file)

            csv = metadata_chats.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()

            st.markdown('<a href="data:file/csv;base64,{}" download="collected_chats.csv" title="Download collected_chats.csv">Collected Chats</a>'.format(b64), unsafe_allow_html=True)

        with open(metadata_counter_csv_file, 'rb') as file:
            metadata_counter = read_csv(metadata_counter_csv_file)

            csv = metadata_counter.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()

            st.markdown('<a href="data:file/csv;base64,{}" download="counter.csv" title="Download counter.csv">Counter</a>'.format(b64), unsafe_allow_html=True)

    #dataset
    with tab3:
        st.subheader('dataset (.csv)')
        dataset_csv_file = 'output/data/msgs_dataset.csv'

        with open(dataset_csv_file, 'rb') as file:
            df = read_csv(dataset_csv_file)

            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()

            st.markdown('<a href="data:file/csv;base64,{}" download="msgs_dataset.csv.csv" title="Download msgs_dataset.csv">Dataset</a>'.format(b64), unsafe_allow_html=True)

            st.dataframe(df)

    #restart
    with tab4:
        restart = st.button('restart', type='primary')

        if restart:
            st.experimental_rerun()