import asyncio
import requests
import json

from mapping import map_data

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'loggers': {
        'quart.app': {
            'level': 'INFO',
        },
    },
})

class Cache:
    def __init__(self, app):
        self.data = None
        self.app = app

    async def load_data(self):
        while True:
            try:
                loop = asyncio.get_running_loop()
                source = self.app.config['SOURCE']
                self.app.logger.info('Requesting {}'.format(source))
                result = await loop.run_in_executor(None, requests.get, source)
                self.app.logger.info('Data received')
                self.data = map_data(source, self.app.config['BASE_URI'], json.loads(result.text))
            except Exception as e:
                self.app.logger.error(e)
            finally:
                await asyncio.sleep(5 * 60)
