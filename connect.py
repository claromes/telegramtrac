import argparse
import asyncio

from api import *
from utils import get_config_attrs

parser = argparse.ArgumentParser(description='Arguments.')

args = vars(parser.parse_args())
config_attrs = get_config_attrs()

args = {**args, **config_attrs}

sfile = 'session_file'
***REMOVED*** args['api_id']
***REMOVED*** args['api_hash']
***REMOVED*** args['phone']

loop = asyncio.get_event_loop()

client = loop.run_until_complete(
	get_connection(sfile, api_id, api_hash, phone)
)