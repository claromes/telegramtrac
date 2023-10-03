# -*- coding: utf-8 -*-

'''
Copyright (c) Clarissa R Mendes (claromes) (2023)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import streamlit as st
from streamlit_extras.customize_running import center_running
import subprocess
import json
import configparser
from pandas import read_csv, read_excel
import base64
from io import BytesIO
import os
import asyncio
import shutil

from telegram_tracker import (api, cryptography)

__version__ = '0.6'

# page config
st.set_page_config(
    page_title='telegramtrac',
    page_icon='🟦',
    layout='centered',
    initial_sidebar_state='collapsed',
    menu_items={
        'About': '''
        ### 🟦 telegramtrac

        A browser interface to Telegram's API. Provides modules for connecting, signing in and communicating via Telethon. Generates files containing messages and metadata. It also includes additional modules for generating datasets and network graphs.

        [![GitHub release (latest by date including pre-releases](https://img.shields.io/github/v/release/claromes/telegramtrac?include_prereleases)](https://github.com/claromes/telegramtrac/releases) [![License](https://img.shields.io/github/license/claromes/telegramtrac)](https://github.com/claromes/telegramtrac/blob/main/LICENSE.txt)

        -------
        ''',
        'Get help': 'https://github.com/claromes/telegramtrac#usage',
        'Report a bug': 'https://github.com/claromes/telegramtrac/issues',
    }
)

# components variables
title_component = st.empty()
form_component = st.empty()
sign_in_component = st.empty()
channel_component = st.empty()
form_component_channel = st.empty()
center_running()

trac = ''
error_connect = False

# states
if 'channel_name' not in st.session_state:
    st.session_state['channel_name'] = ''

if 'password_value' not in st.session_state:
    st.session_state['password_value'] = ''

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

def delete():
    # delete this and add log_out https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.auth.AuthMethods.log_out or ResetAuthorizationsRequest()
    st.session_state.api_id = ''
    st.session_state.api_hash = ''
    st.session_state.phone = ''
    st.session_state.code_value = ''
    st.session_state.code_state = ''
    st.session_state.password_value = ''
    st.session_state.restart = False

    # try:
    os.remove(f'config/config_{st.session_state.api_id}.ini')
    os.remove(f'sign_in/encrypted_code_{st.session_state.api_id}.bin')
    os.remove(f'sign_in/encrypted_password_{st.session_state.api_id}.bin')
    os.remove(f'session/session_file_{st.session_state.api_id}.session')

    file_path_session_journal = f'session/session_file_{st.session_state.api_id}.session-journal'
    if os.path.exists(file_path_session_journal):
        os.remove(file_path_session_journal)
    
    dir_path_output_data = f'output_{st.session_state.api_id}'
    if os.path.exists(dir_path_output_data):
        os.rmdir(dir_path_output_data)

    st.success('Session files deleted.')
    # except:
    #     st.error('Missing files')

# title
title_component.title("""
telegramtrac

Browser interface to Telegram's API with additional modules for generating datasets and network graphs
""", help=f'{__version__} (not stable)', anchor=False)

if not st.session_state.restart:
    # credentials
    with form_component.form(key='config_form'):
        api_id = st.text_input('api_id', placeholder='12349876')
        api_hash = st.text_input('api_hash', placeholder='123a456s789d987h654g321q987w12f0')
        phone = st.text_input('phone', placeholder='+5500912348765')

        config = {
            'api_id': api_id,
            'api_hash': api_hash,
            'phone': phone
        }

        if st.session_state.api_id == '':
            st.session_state.api_id = api_id

        # credentials options buttons
        col1, col2, _ = st.columns([3, 4, 6])

        with col1:
            send_credentials = st.form_submit_button('send credentials', type='primary')
        with col2:
            st.link_button('create API credentials', 'https://my.telegram.org/auth')

    if send_credentials and (api_id == '' or api_hash == '' or phone == ''):
        st.error('Something went wrong.')

    if send_credentials and api_id != '' and api_hash != '' and phone != '':
        center_running()

        config_parser = configparser.ConfigParser()
        config_parser['Telegram API credentials'] = config
        with open(f'config/config_{st.session_state.api_id}.ini', 'w') as file:
            config_parser.write(file)
            file.close()

        st.session_state.code_state = True

        try:
            # avoid Streamlit Cloud ModuleNotFoundError
            # if st.get_option('server.port') == 8501:
            #     cmd_tele = "pip install telethon==1.26.1 --user"
            #     output = subprocess.check_output(cmd_tele.split())

            #     cmd_pd = "pip install pandas==1.5.3 --user"
            #     output = subprocess.check_output(cmd_pd.split())

            #     cmd_tqdm = "pip install tqdm==4.64.1 --user"
            #     output = subprocess.check_output(cmd_tqdm.split())

            #     cmd_open = "pip install openpyxl==3.0.10 --user"
            #     output = subprocess.check_output(cmd_open.split())

            #     cmd_pycrypto = "pip install pycryptodome==3.17 --user"
            #     output = subprocess.check_output(cmd_pycrypto.split())

            # connect to API
            print('python connect.py')

            cmd_connect = f'python connect.py --api_id {str(st.session_state.api_id)}'
            subprocess.check_output(cmd_connect.split())
        except:
            sign_in_component.error('Something went wrong.')
            error_connect = True

    # sign in code
    with sign_in_component.form(key='config_sign_in_form'):
        if st.session_state.code_state and not error_connect:
            sign_in_code = st.text_input('code', disabled=False, value=st.session_state.code_value, placeholder='54321')
            password = st.text_input('password', disabled=False, value=st.session_state.password_value, type='password', help='optional')
        else:
            sign_in_code = st.text_input('code', disabled=True, value=st.session_state.code_value)
            password = st.text_input('password', disabled=True, value=st.session_state.password_value)

        if sign_in_code == '':
            sign_in_code = st.session_state.code_value

        if password == '':
            password = st.session_state.password_value

        if st.session_state.code_state and not error_connect:
            sign_in = st.form_submit_button('sign in', disabled=False, type='primary')
        else:
            sign_in = st.form_submit_button('sign in', disabled=True, type='primary')

        if sign_in:
            center_running()
            st.session_state.code_value = sign_in_code
            st.session_state.password_value = password
            st.session_state.code_state = True

            # encrypt code and password
            cryptography.crypt_code(sign_in_code, st.session_state.api_id)
            cryptography.crypt_password(password, st.session_state.api_id)

            # sign in to API
            try:
                print('python sign_in.py')
                cmd_sign_in = f'python sign_in.py --api_id {str(st.session_state.api_id)}'
                subprocess.check_output(cmd_sign_in.split())
            except:
                sign_in_component.error('Something went wrong.')
                st.session_state.code_state == False

    # channel name
    with channel_component.form(key='channel_form'):
        if sign_in and st.session_state.code_state == True:
            channel_name = st.text_area('channels (semicolon separated)', placeholder='channel_name_1;channel_name_2;channel_name_3;channel_name_4;...', disabled=False, key='channel_name', help='t.me/channel_name')
            trac = st.form_submit_button('trac', disabled=False, type='primary')
            send_credentials = True
        else:
            channel_name = st.text_area('channels (semicolon separated)', disabled=True)
            trac = st.form_submit_button('trac', disabled=True, type='primary')
            send_credentials = True
else:
    form_component.empty()
    sign_in_component.empty()
    channel_component.empty()

    st.button('delete session files', on_click=delete, type='secondary', use_container_width=True)

# data
if trac or st.session_state.channel_name != '':
    center_running()
    form_component.empty()
    sign_in_component.empty()
    channel_component.empty()
    form_component_channel.empty()
    st.session_state.restart = True

    channel_name = st.session_state.channel_name
    channels = channel_name.split(';')
    channels = [channel_name.strip() for channel_name in channels]
    channels = list(filter(bool, channels))

    telegram_channel_args = ''
    for channel in channels:
        telegram_channel_args += f'--telegram-channel {channel} '

    try:
        output_folder = f'output_{st.session_state.api_id}/'

        print('python main.py --telegram-channel')
        cmd_main = f'python main.py {telegram_channel_args} --output {output_folder} --api_id {st.session_state.api_id}'
        subprocess.check_output(cmd_main.split())
    except:
        st.error('Something went wrong.')
        st.session_state.restart = False

    try:
        print('python build-datasets.py')
        cmd_dataset = f'python build-datasets.py --data-path {output_folder}'
        subprocess.check_output(cmd_dataset.split())
    except:
        st.error('Something went wrong.')

    try:
        dir_path_output_data = os.path.join(f'output_{st.session_state.api_id}')

        if os.path.exists(dir_path_output_data):
            subdirectories = [entry for entry in os.scandir(dir_path_output_data) if entry.is_dir()]

        if subdirectories:
            print('python channels-to-network.py')
            cmd_channels_to_network = f'python channels-to-network.py --data-path {output_folder}'
            subprocess.check_output(cmd_channels_to_network.split())
    except:
        st.error('Something went wrong.')

    # tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['messages', 'metadata', 'network',  'dataset', 'options'])

    # messages
    with tab1:
        try:
            for channel in channels:
                st.subheader(f'{channel} messages', anchor=False)
                json_file = f'output_{st.session_state.api_id}/{channel}/{channel}_messages.json'

                with open(json_file, 'rb') as file:
                    data = json.load(file)

                json_dump = json.dumps(data)
                b64 = base64.b64encode(json_dump.encode()).decode()
                href = f'data:file/json;base64,{b64}'

                st.markdown(f'<a href="{href}" download="{channel}_messages.json" title="Download {channel}_messages.json">{channel}_messages.json</a>', unsafe_allow_html=True)
                st.json(data, expanded=False)
        except:
            st.error('Something went wrong.')

    # metadata
    with tab2:
        try:
            for channel in channels:
                metadata_json_file = f'output_{st.session_state.api_id}/{channel}/{channel}.json'
                metadata_txt_file = f'output_{st.session_state.api_id}/chats.txt'
                metadata_chats_csv_file = f'output_{st.session_state.api_id}/collected_chats.csv'
                metadata_chats_xlsx_file = f'output_{st.session_state.api_id}/collected_chats.xlsx'
                metadata_counter_csv_file = f'output_{st.session_state.api_id}/counter.csv'
                user_exceptions_txt_file = f'output_{st.session_state.api_id}/user_exceptions.txt'

                st.subheader(f'{channel} metadata', anchor=False)

                with open(metadata_json_file, 'rb') as file:
                    data = json.load(file)

                json_dump = json.dumps(data)

                b64 = base64.b64encode(json_dump.encode()).decode()
                href = f'data:file/json;base64,{b64}'

                st.markdown(f'<a href="{href}" download="{channel}.json" title="Download {channel}.json">{channel}.json</a>', unsafe_allow_html=True)

                with open(metadata_txt_file, 'rb') as file:
                    txt = file.read().decode()

                b64 = base64.b64encode(txt.encode()).decode()
                href = f'data:file/txt;base64,{b64}'

                st.markdown(f'<a href="{href}" download="chats.txt" title="Download chats.txt">chats.txt</a>', unsafe_allow_html=True)

                with open(metadata_chats_csv_file, 'rb'):
                    metadata_chats = read_csv(metadata_chats_csv_file)

                csv = metadata_chats.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()

                st.markdown(f'<a href="data:file/csv;base64,{b64}" download="collected_chats.csv" title="Download collected_chats.csv">collected_chats.csv</a>', unsafe_allow_html=True)

                with open(metadata_chats_xlsx_file, 'rb'):
                    metadata_chats_xlsx = read_excel(metadata_chats_xlsx_file)

                xlsx = BytesIO()
                metadata_chats_xlsx.to_excel(xlsx, index=False, engine='openpyxl')
                xlsx.seek(0)
                b64 = base64.b64encode(xlsx.read()).decode()

                st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="collected_chats.xlsx" title="Download collected_chats.xlsx">collected_chats.xlsx</a>', unsafe_allow_html=True)

                with open(metadata_counter_csv_file, 'rb'):
                    metadata_counter = read_csv(metadata_counter_csv_file)

                csv = metadata_counter.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()

                st.markdown(f'<a href="data:file/csv;base64,{b64}" download="counter.csv" title="Download counter.csv">counter.csv</a>', unsafe_allow_html=True)

                if os.path.exists(user_exceptions_txt_file):
                    with open(user_exceptions_txt_file, 'rb') as file:
                        user_txt = file.read().decode()

                    b64 = base64.b64encode(user_txt.encode()).decode()
                    href = f'data:file/txt;base64,{b64}'

                    st.markdown(f'<a href="{href}" download="user_exceptions.txt" title="Download user_exceptions.txt">user_exceptions.txt</a>', unsafe_allow_html=True)
        except:
            st.error('Something went wrong.')

    # network
    with tab3:
        try:
            network_image_file = f'output_{st.session_state.api_id}/network.png'
            network_gexf_file = f'output_{st.session_state.api_id}/graph.gexf'

            with open(network_image_file, 'rb') as img_file:
                img_data = img_file.read()

            b64 = base64.b64encode(img_data).decode()
            href = f'data:image/png;base64,{b64}'

            st.image(img_data)
            st.markdown(f'<a href="{href}" download="network.png" title="Download network.png">network.png</a>', unsafe_allow_html=True)
            
            with open(network_gexf_file, 'rb') as gexf_file:
                gexf_data = gexf_file.read()

            b64 = base64.b64encode(gexf_data).decode()
            href = f'data:application/gexf+xml;base64,{b64}'

            st.markdown(f'<a href="{href}" download="graph.gexf" title="Download graph.gexf">graph.gexf</a>', unsafe_allow_html=True)
        except:
            st.error('Something went wrong.')

    # dataset
    with tab4:
        try:
            st.subheader('messages from all requested channels', anchor=False)
            dataset_csv_file = f'output_{st.session_state.api_id}/msgs_dataset.csv'

            with open(dataset_csv_file, 'rb'):
                df = read_csv(dataset_csv_file)

            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'data:file/csv;base64,{b64}'

            st.markdown(f'<a href="{href}" download="msgs_dataset.csv" title="Download msgs_dataset.csv">msgs_dataset.csv</a>', unsafe_allow_html=True)

            st.dataframe(df)
        except:
            st.error('Something went wrong.')
        
    # options - delete session files
    with tab5:
        st.button('delete session files', on_click=delete, type='secondary', use_container_width=True)
