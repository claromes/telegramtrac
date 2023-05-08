import argparse
import asyncio

from api import get_connection
from utils import get_config_attrs

parser = argparse.ArgumentParser(description='Arguments.')
parser.add_argument(
	'--api_id',
	'-o',
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

phone_code_hash = loop.run_until_complete(
	get_connection(sfile, api_id, api_hash, phone)
)