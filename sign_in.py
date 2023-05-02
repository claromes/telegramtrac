import asyncio

from api import client_sign_in
from connect import (sfile, api_id, api_hash, phone, phone_code_hash)

loop = asyncio.get_event_loop()

client = loop.run_until_complete(
	client_sign_in(sfile, api_id, api_hash, phone, phone_code_hash)
)