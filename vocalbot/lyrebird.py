"""
https://docs.lyrebird.ai/reference-avatar/api.html
"""
import os
import httpx

LYREBIRD_CLIENT_ID = os.environ['LYREBIRD_CLIENT_ID']
LYREBIRD_CLIENT_SECRET = os.environ['LYREBIRD_CLIENT_SECRET']

class Lyrebird():
    """a httpx lyrebird.ai client"""
