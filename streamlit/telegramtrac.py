import streamlit as st
from streamlit_extras.customize_running import center_running
import subprocess
import json
import configparser
from pandas import read_csv
import base64
import os

#page config
st.set_page_config(
    page_title="telegramtrac",
    page_icon="🟦",
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
form_component_channel = st.empty()
center_running()

trac = ''
new_trac = ''

#states
if 'channel_name' not in st.session_state:
    st.session_state['channel_name'] = ''

if 'code_state' not in st.session_state:
    st.session_state['code_state'] = False

if 'code_value' not in st.session_state:
    st.session_state['code_value'] = ''

if 'api_id' not in st.session_state:
    st.session_state['api_id'] = ''

if 'api_hash' not in st.session_state:
    st.session_state['api_hash'] = ''

if 'phone' not in st.session_state:
    st.session_state['phone'] = ''

if 'restart' not in st.session_state:
    st.session_state['restart'] = False

print(st.session_state.restart)

#title
title_component.title('telegramtrac', help="not stable", anchor=False)

if not st.session_state.restart:
    #credentials
    with form_component.form(key='config_form'):
        api_id = st.text_input('api_id')
        api_hash = st.text_input('api_hash')
        phone = st.text_input('phone')

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
        #     cmd_tele = "pip install telethon --user"
        #     output = subprocess.check_output(cmd_tele.split())

        #     cmd_pd = "pip install pandas --user"
        #     output = subprocess.check_output(cmd_pd.split())

        #     cmd_tqdm = "pip install tqdm --user"
        #     output = subprocess.check_output(cmd_tqdm.split())

        #     cmd_open = "pip install openpyxl --user"
        #     output = subprocess.check_output(cmd_open.split())

        #     cmd_connect = 'python connect.py'
        #     output = subprocess.check_output(cmd_connect.split())
        # except subprocess.CalledProcessError:
        #     pass
        # except Exception:
        #     pass

    #sign in code
    with sign_in_component.form(key='config_sign_in_form'):
        if st.session_state.code_state:
            code_sign_in = st.text_input('code', disabled=False)
        else:
            code_sign_in = st.text_input('code', disabled=True)

        if code_sign_in == '':
            code_sign_in = st.session_state.code_value

        config_sign_in_code = {
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
else:
    form_component.empty()
    sign_in_component.empty()
    channel_component.empty()

    with form_component_channel.form(key='config_form_channel'):
        #send same credentials and code
        api_id = st.session_state.api_id
        api_hash = st.session_state.api_hash
        phone = st.session_state.phone
        code = st.session_state.code_value

        st.session_state.channel_name = st.text_input('channel name', placeholder="https://t.me/CHANNEL_NAME_IS_HERE", disabled=False, key='channel_name_new_trac')
        new_trac = st.form_submit_button('new trac', disabled=False, type='primary')

print(new_trac, 'trac')
print(st.session_state.channel_name)
#data tabs
if trac or new_trac and st.session_state.channel_name != '':
    center_running()
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['messages', 'metadata', 'dataset', 'network', 'new trac'])

    form_component.empty()
    sign_in_component.empty()
    channel_component.empty()
    form_component_channel.empty()

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

    path = 'output/data'
    subdirectories = [entry for entry in os.scandir(path) if entry.is_dir()]
    path_lens = len(subdirectories) > 1

    # if path_lens:
    #     try:
    #         cmd_dataset = 'python channels-to-network.py'
    #         output = subprocess.check_output(cmd_dataset.split())
    #     except subprocess.CalledProcessError:
    #         pass
    #     except Exception:
    #         pass

    #json - main file
    with tab1:
        json_file = 'output/data/{}/{}_messages.json'.format(st.session_state.channel_name, st.session_state.channel_name)

        with open(json_file, 'rb') as file:
            st.subheader('{} messages'.format(st.session_state.channel_name), anchor=False)

            data = json.load(file)
            json_dump = json.dumps(data)
            b64 = base64.b64encode(json_dump.encode()).decode()
            href = 'data:file/json;base64,{}'.format(b64)

            st.markdown('<a href="{}" download="{}_messages.json" title="Download {}_messages.json">{}_messages.json</a>'.format(href, st.session_state.channel_name, st.session_state.channel_name, st.session_state.channel_name), unsafe_allow_html=True)
            st.json(data, expanded=False)

    #metadata
    with tab2:
        metadata_json_file = 'output/data/{}/{}.json'.format(st.session_state.channel_name, st.session_state.channel_name)
        metadata_txt_file = 'output/data/chats.txt'
        metadata_chats_csv_file = 'output/data/collected_chats.csv'
        metadata_counter_csv_file = 'output/data/counter.csv'

        st.subheader('{} metadata'.format(st.session_state.channel_name), anchor=False)
        with open(metadata_json_file, 'rb') as file:
            data = json.load(file)
            json_dump = json.dumps(data)

            b64 = base64.b64encode(json_dump.encode()).decode()
            href = 'data:file/json;base64,{}'.format(b64)

            st.markdown('<a href="{}" download="{}.json" title="Download {}.json">{}.json</a>'.format(href, st.session_state.channel_name, st.session_state.channel_name, st.session_state.channel_name), unsafe_allow_html=True)

        with open(metadata_txt_file, 'rb') as file:
            txt = file.read().decode()

            b64 = base64.b64encode(txt.encode()).decode()
            href = 'data:file/txt;base64,{}'.format(b64)

            st.markdown('<a href="{}" download="chats.txt" title="Download chats.txt">chats.txt</a>'.format(href), unsafe_allow_html=True)

        with open(metadata_chats_csv_file, 'rb') as file:
            metadata_chats = read_csv(metadata_chats_csv_file)

            csv = metadata_chats.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()

            st.markdown('<a href="data:file/csv;base64,{}" download="collected_chats.csv" title="Download collected_chats.csv">collected_chats.csv</a>'.format(b64), unsafe_allow_html=True)

        with open(metadata_counter_csv_file, 'rb') as file:
            metadata_counter = read_csv(metadata_counter_csv_file)

            csv = metadata_counter.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()

            st.markdown('<a href="data:file/csv;base64,{}" download="counter.csv" title="Download counter.csv">counter.csv</a>'.format(b64), unsafe_allow_html=True)

    #dataset
    with tab3:
        st.subheader('dataset', anchor=False)
        #st.caption('Channels: {}'.format(st.session_state.channel_name))
        dataset_csv_file = 'output/data/msgs_dataset.csv'

        with open(dataset_csv_file, 'rb') as file:
            df = read_csv(dataset_csv_file)

            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()

            st.markdown('<a href="data:file/csv;base64,{}" download="msgs_dataset.csv" title="Download msgs_dataset.csv">msgs_dataset.csv</a>'.format(b64), unsafe_allow_html=True)

            st.dataframe(df)

    with tab4:
        if path_lens:
            st.info('Under development')
        else:
            st.info('There is only one channel.')
            #st.info('There is only one channel.')

    #restart
    with tab5:
       st.button('new trac', type='primary')
       st.session_state.restart = True