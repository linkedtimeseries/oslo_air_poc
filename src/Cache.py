import asyncio
import requests
import json

from mapping.oslo import OsloMapper
from mapping.smart_data_models import SDMMapper


models = {
    'oslo': OsloMapper,
    'smart_data_models': SDMMapper,
}

class Cache:
    """
    Proxy cache for the luftdaten APIs.
    It periodically requests new data, and stores the mapped results until the next iteration.
    """

    def __init__(self, app):
        self.data = {}
        self.app = app

    def get_data(self, model):
        return self.data.get(model, {})

    async def load_data(self, interval = 5 * 60):
        while True:
            try:
                loop = asyncio.get_running_loop()
                source = self.app.config['SOURCE']
                self.app.logger.info('Requesting {}'.format(source))
                result = await loop.run_in_executor(None, requests.get, source)
                self.app.logger.info('Data received')

                raw = json.loads(result.text)
                for model, mapper in models.items():
                    self.data[model] = json.dumps(mapper.map_data(source, self.app.config['BASE_URI'], raw))
            except Exception as e:
                self.app.logger.error(e)
            finally:
                self.app.logger.info('Sleeping for {}s'.format(interval))
                await asyncio.sleep(interval)
