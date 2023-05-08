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
