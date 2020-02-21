import asyncio
import logging

from fastapi import FastAPI
import httpx
from starlette.responses import HTMLResponse, RedirectResponse, StreamingResponse, JSONResponse
from starlette.websockets import WebSocket

from pydantic import BaseModel



from .lyrebird import get_login_url, generate_audio, get_audio
from .pandorabots import chat as pandorabots_chat

logger = logging.getLogger(__name__)


class Text(BaseModel):
    text: str

def make_app():
    logger.info('creating the FastAPI app...')
    app = FastAPI()

    with open("static/index.html") as f:
        index_html = f.read()
    login_url = get_login_url(scope='voice')
    logger.info('login_url = %s', login_url)

    httpx_client = httpx.AsyncClient()


    @app.get("/")
    async def index():
        return HTMLResponse(index_html)

    @app.get('/chataudio')
    async def chataudio(text: str):
        chat_text = await pandorabots_chat(httpx_client, text)
        audio = await generate_audio(httpx_client, chat_text['that']) 
        return StreamingResponse(audio)
    @app.post('/chat')
    async def chat(text: Text):
        resp = await pandorabots_chat(httpx_client, text.text)
        return JSONResponse(resp)

    @app.post('/sayit')
    async def sayit(text: Text):
        resp = await generate_audio(httpx_client, text.text)
        #resp = await get_audio(httpx_client)
        if isinstance(resp, dict):
            return JSONResponse(resp, status_code=resp.get('status_code', 200))
        return StreamingResponse(resp)
        


    @app.get('/login')
    async def login():
        return RedirectResponse(login_url)
        
    @app.websocket("/ws/")
    async def websocket_endpoint(ws: WebSocket):
        await ws.accept()

        while True:
            text = await ws.receive_text()
            #resp = await generate_audio(httpx_client, text)
            resp = await get_audio(httpx_client)
            logger.info('resp = %s', resp)
        logger.info('ws disconnected')
    logger.info('FastAPI app created')
    return app
