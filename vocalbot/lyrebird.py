"""
https://docs.lyrebird.ai/reference-avatar/api.html
"""
import io
import logging
import os
from json.decoder import JSONDecodeError
import random
import string
from urllib.parse import urlencode

import httpx

LYREBIRD_CLIENT_ID = os.environ['LYREBIRD_CLIENT_ID']
LYREBIRD_CLIENT_SECRET = os.environ['LYREBIRD_CLIENT_SECRET']
LYREBIRD_REDIRECT_URI = os.environ['LYREBIRD_REDIRECT_URI']
LYREBIRD_ACCESS_TOKEN = os.getenv('LYREBIRD_ACCESS_TOKEN')

logger = logging.getLogger(__name__)

def _get_random():
    all_letters =  string.ascii_letters + string.digits 
    return ''.join([random.choice(all_letters) for _ in range(5)])

def get_login_url(scope):
    params = {
        'response_type': 'token',
        'redirect_uri': LYREBIRD_REDIRECT_URI,
        'client_id': LYREBIRD_CLIENT_ID,
        'scope': scope,
        'state': _get_random(),
    }

    return f'https://myvoice.lyrebird.ai/authorize?{urlencode(params)}'

async def _call(client: httpx.AsyncClient, endpoint, method='GET', **params):
    coro = getattr(client, method.lower())
    headers = {
        'Authorization': f'Bearer {LYREBIRD_ACCESS_TOKEN}',
    }
    url = f'https://avatar.lyrebird.ai/api/v0/{endpoint}'
    #url = f'https://beta.myvoice.lyrebird.ai/api/v0/{endpoint}'

    logger.info('%s %s', method, url)
    if method == 'GET':
        resp = await coro(url, headers=headers, params=params)
    else:
        resp = await coro(url, headers=headers, **params)

    try:
        data = resp.json()
    except JSONDecodeError:
        data = io.BytesIO(resp.content)
    if resp.status_code >= 400:
        logger.error('response status = %d', resp.status_code)
        if isinstance(data, dict):
            data['status_code'] = resp.status_code
    return data


async def get_audio(client):
    return await _call(client, 'utterances', method='GET')

async def generate_audio(client: httpx.AsyncClient, text: str):
    logger.info('generate_audio for text "%s"', text)
    return await _call(client, 'generate', method='POST', json={'text': text})

