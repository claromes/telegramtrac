import argparse
import asyncio

from api import *
from utils import get_config_attrs

parser = argparse.ArgumentParser(description='Arguments.')

args = vars(parser.parse_args())
config_attrs = get_config_attrs()

args = {**args, **config_attrs}

api_id = args['api_id']
api_hash = args['api_hash']
phone = args['phone']
sfile = 'session_file_{}'.format(api_id)

loop = asyncio.get_event_loop()

phone_code_hash = loop.run_until_complete(
	get_connection(sfile, api_id, api_hash, phone)
)