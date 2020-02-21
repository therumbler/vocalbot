import httpx
import json
#from lib.caching import cacheable

BASE_URL = 'https://pandorabots.com/pandora/talk-xml'
BOTID = 'da4d216c0e345aa1'


#@cacheable(expire=3600)
async def _call(client, *args, **kwargs):
    if 'format' not in kwargs:
        kwargs['format'] = 'json'
    if 'botid' not in kwargs:
        kwargs['botid'] =  BOTID
        response = await client.get(BASE_URL, params=kwargs)
    return response.json()

async def chat(client, input_text):
    response = await _call(client, input=input_text)
    return response

def main():
    """Let's do something"""
    input_text = 'Hi, how are you?'
    response = chat(input_text)
    print(json.dumps(response, indent=2))

if __name__ == '__main__':
    main()
