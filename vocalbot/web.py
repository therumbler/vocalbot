import asyncio
import logging
from fastapi import FastAPI
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.websockets import WebSocket

from .lyrebird import Lyrebird

logger = logging.getLogger(__name__)


def make_app():
    logger.info('creating the FastAPI app...')
    app = FastAPI()

    with open("static/index.html") as f:
        index_html = f.read()

    @app.get("/")
    async def index():
        return HTMLResponse(index_html)

    @app.get('/login')
    async def login():
        return 
    @app.websocket("/ws/")
    async def websocket_endpoint(ws: WebSocket):
        await ws.accept()

        while True:
            msg = await ws.receive_text()
            logger.debug('got msg %s', msg)
            if msg == 'kill':
                logger.info('setting kill_event')
        logger.info('ws disconnected')
    logger.info('FastAPI app created')
    return app
