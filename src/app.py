from quart import Quart, render_template, websocket, Response

import asyncio
import toml

from Cache import Cache

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'loggers': {
        'quart.app': {
            'level': 'INFO',
        },
    },
})

app = Quart(__name__)
app.config.from_file("config.toml", load=toml.load)

cache = Cache(app)

@app.route("/<model>")
async def main(model):
    global cache
    resp = Response(cache.get_data(model))
    resp.headers['Content-Type'] = 'application/ld+json'
    return resp

@app.before_serving
async def startup():
    global cache
    loop = asyncio.get_event_loop()
    loop.create_task(cache.load_data(app.config['POLLING_INTERVAL']))

if __name__ == "__main__":
    app.run()
