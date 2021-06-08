from quart import Quart, render_template, websocket, Response
from quart_compress import Compress

import asyncio
import json

from Cache import Cache

app = Quart(__name__)
app.config.from_file("config.json", load=json.load)
Compress(app)

cache = Cache(app)

@app.route("/")
async def main():
    global cache
    resp = Response(json.dumps(cache.data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/ld+json'
    return resp

@app.before_serving
async def startup():
    global cache
    loop = asyncio.get_event_loop()
    loop.create_task(cache.load_data())



if __name__ == "__main__":
    
    app.run()
    

    
    # loop.run_forever()
