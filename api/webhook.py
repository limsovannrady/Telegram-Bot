import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
from http.server import BaseHTTPRequestHandler
from telegram import Update
from bot import create_app


async def process_update(update_data: dict):
    application = create_app()
    async with application:
        await application.process_update(
            Update.de_json(update_data, application.bot)
        )


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            update_data = json.loads(body.decode("utf-8"))
            asyncio.run(process_update(update_data))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot webhook is active.")

    def log_message(self, format, *args):
        pass
