import streamlit as st
from streamlit_extras.customize_running import center_running
import subprocess
import json
import configparser
from pandas import read_csv
import base64
import os
import shutil

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

#page config
st.set_page_config(
    page_title="telegramtrac",
    page_icon="🟦",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={

        'About': """
        telegramtrac is web-based tool designed for tracking public channels on Telegram.

        The tool is part of Bellingcat's April 2023 Hackathon. It's a fork of the package [`telegram-tracker`](https://github.com/estebanpdl/telegram-tracker) developed by Esteban Ponce de León, DFRLab researcher.

        -------
        """,
        'Get help': 'https://github.com/claromes/telegramtrac#workflow',
        'Report a bug': 'https://github.com/claromes/telegramtrac/issues',

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
error_connect = False

#states
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

#encrypt code and password
def crypt_code(code):
    key = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_EAX)

    sign_in_code = code.encode()

    ciphertext, tag = cipher.encrypt_and_digest(sign_in_code)

    file_out = open('sign_in/encrypted_code_{}.bin'.format(api_id), 'wb')
    for i in (key, cipher.nonce, tag, ciphertext):
        file_out.write(i)
    file_out.close()

def crypt_password(password):

    key = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_EAX)

    sign_in_password = password.encode()

    ciphertext, tag = cipher.encrypt_and_digest(sign_in_password)

    file_out = open('sign_in/encrypted_password_{}.bin'.format(api_id), 'wb')
    for i in (key, cipher.nonce, tag, ciphertext):
        file_out.write(i)
    file_out.close()

#delete .session and .bin files
def delete_files_restores_app():
    #delete this and add log_out https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.auth.AuthMethods.log_out or ResetAuthorizationsRequest()
    try:
        os.remove('config/config_{}.ini'.format(api_id))
        os.remove('sign_in/encrypted_code_{}.bin'.format(api_id))
        os.remove('sign_in/encrypted_password_{}.bin'.format(api_id))
        #os.remove('session_file_{}.session'.format(api_id))

        st.success('Session files deleted.')
        st.session_state.api_id = ''
        st.session_state.api_hash = ''
        st.session_state.phone = ''
        st.session_state.code_value = ''
        st.session_state.password_value = ''
        st.session_state.restart = False
    except:
        st.error('Missing files')

#title
if st.session_state.code_state == False:
    title_component.title("""
telegramtrac

Web-based tool designed for tracking public channels on Telegram

*:blue[Create your API credentials [here](https://my.telegram.org/auth)]*
""", help='v0.4.0', anchor=False)
else:
    title_component.title("""
telegramtrac

Web-based tool designed for tracking public channels on Telegram
""", help='v0.4.0', anchor=False)

#changelog and roadmap
with st.sidebar:
    st.markdown("""

# Roadmap

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

# Changelog

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

    """)

if not st.session_state.restart:
    #delete all files and directories before start another tracking
    # dir_path_output = os.path.join('output')

    # if os.path.exists(dir_path_output):
    #     shutil.rmtree(dir_path_output)

    #credentials
    with form_component.form(key='config_form'):
        api_id = st.text_input('api_id', placeholder='12349876')
        api_hash = st.text_input('api_hash', placeholder='123a456s789d987h654g321q987w12f0')
        phone = st.text_input('phone', placeholder='+5500912348765')

        config = {
            'api_id': api_id,
            'api_hash': api_hash,
            'phone': phone
        }

        send_credentials = st.form_submit_button('send credentials', type='primary')

    if send_credentials and (api_id == '' or api_hash == '' or phone == ''):
        st.error('Something went wrong.')

    if send_credentials and api_id != '' and api_hash != '' and phone != '':
        center_running()

        config_parser = configparser.ConfigParser()
        config_parser['Telegram API credentials'] = config
        with open('config/config_{}.ini'.format(api_id), 'w') as file:
            config_parser.write(file)
            file.close()

        st.session_state.code_state = True

        # try:
        #     #avoid streamlit errors
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

        #     #connect to API
        #     print('python connect.py')
        #     cmd_connect = 'python connect.py'
        #     subprocess.check_output(cmd_connect.split())
        # except:
        #     form_component.error('Something went wrong.')
        #     error_connect = True

    #sign in code
    with sign_in_component.form(key='config_sign_in_form'):
        if st.session_state.code_state and not error_connect:
            sign_in_code = st.text_input('code', disabled=False, value=st.session_state.code_value, placeholder='54321')
            password = st.text_input('password', disabled=False, value=st.session_state.password_value, type='password', placeholder='Two-Step Verification enabled users')
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

            #encrypt code and password
            crypt_code(sign_in_code)
            crypt_password(password)

            #sign in to API
            # try:
            #     print('python sign_in.py')
            #     cmd_sign_in = 'python sign_in.py'
            #     subprocess.check_output(cmd_sign_in.split())
            # except:
            #     st.error('Something went wrong.')
            #     st.session_state.code_state == False

    #channel name
    with channel_component.form(key='channel_form'):
        if sign_in and st.session_state.code_state == True or st.session_state.channel_name != '':
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
        #send same credentials, code and password
        api_id = st.session_state.api_id
        api_hash = st.session_state.api_hash
        phone = st.session_state.phone
        code = st.session_state.code_value
        password = st.session_state.password_value

        st.session_state.channel_name = st.text_input('channel name', placeholder="https://t.me/CHANNEL_NAME_IS_HERE", disabled=False, key='channel_name_new_trac')
        new_trac = st.form_submit_button('new trac', disabled=False, type='primary')

#data tabs
if trac or new_trac and st.session_state.channel_name != '':
    center_running()
    tab1, tab2, tab3, tab4 = st.tabs(['messages', 'metadata', 'dataset', 'options'])

    form_component.empty()
    sign_in_component.empty()
    channel_component.empty()
    form_component_channel.empty()
    st.session_state.restart = True

    # try:
    #     print('python main.py --telegram-channel')
    #     cmd_main = 'python main.py --telegram-channel {}'.format(st.session_state.channel_name)
    #     subprocess.check_output(cmd_main.split())
    # except:
    #     st.error('Something went wrong.')
    #     st.session_state.restart = False

    try:
        print('python build-datasets.py')
        cmd_dataset = 'python build-datasets.py'
        subprocess.check_output(cmd_dataset.split())
    except:
        st.error('Something went wrong.')

    # try:
    #     if os.path.exists(dir_path_output):
    #         path = 'output/data'
    #         subdirectories = [entry for entry in os.scandir(path) if entry.is_dir()]
    #         path_lens = len(subdirectories) > 1
    # except:
    #     st.error('Something went wrong.')

    #json - main file
    with tab1:
        try:
            json_file = 'output/data/{}/{}_messages.json'.format(st.session_state.channel_name, st.session_state.channel_name)

            with open(json_file, 'rb') as file:
                st.subheader('{} messages'.format(st.session_state.channel_name), anchor=False)

                data = json.load(file)
                json_dump = json.dumps(data)
                b64 = base64.b64encode(json_dump.encode()).decode()
                href = 'data:file/json;base64,{}'.format(b64)

                st.markdown('<a href="{}" download="{}_messages.json" title="Download {}_messages.json">{}_messages.json</a>'.format(href, st.session_state.channel_name, st.session_state.channel_name, st.session_state.channel_name), unsafe_allow_html=True)
                st.json(data, expanded=False)
        except:
            st.error('Something went wrong.')

    #metadata
    with tab2:
        try:
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
        except:
            st.error('Something went wrong.')

    #dataset
    with tab3:
        try:
            st.subheader('messages from all requested channels', anchor=False)
            dataset_csv_file = 'output/data/msgs_dataset.csv'

            with open(dataset_csv_file, 'rb') as file:
                df = read_csv(dataset_csv_file)

                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()

                st.markdown('<a href="data:file/csv;base64,{}" download="msgs_dataset.csv" title="Download msgs_dataset.csv">msgs_dataset.csv</a>'.format(b64), unsafe_allow_html=True)

                st.dataframe(df)
        except:
            st.error('Something went wrong.')

    #network
    # with tab4:
    #     st.info('Under development')

    #options - new trac or log out
    with tab4:
        st.button('new trac', type='primary', use_container_width=True)
        st.button('log out', on_click=delete_files_restores_app, type='secondary', use_container_width=True)