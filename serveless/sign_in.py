# -*- coding: utf-8 -*-

'''
Copyright (c) Esteban Ponce de León (2023)
Modified by Clarissa R Mendes

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

import argparse
import asyncio

from telegram_tracker.api import client_sign_in
from telegram_tracker.utils import get_config_attrs

from connect import phone_code_hash

parser = argparse.ArgumentParser(description='Arguments.')
parser.add_argument(
	'--api_id',
	type=str,
	required=False,
)

args_api_id = vars(parser.parse_args())

api_id_str = args_api_id['api_id']

config_attrs = get_config_attrs(api_id_str)

args = {**config_attrs}

api_id = args['api_id']
api_hash = args['api_hash']
phone = args['phone']
sfile = 'session/session_file_{}'.format(api_id)

loop = asyncio.get_event_loop()

client = loop.run_until_complete(
	client_sign_in(sfile, api_id, api_hash, phone, phone_code_hash)
)
