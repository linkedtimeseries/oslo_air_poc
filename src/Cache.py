import asyncio
import requests
import json

from random import sample

from mapping.oslo import OsloMapper
from mapping.smart_data_models import SDMMapper
from mapping.smart_data_models_kv import SDMMapperKV
from mapping.json_ld_star import JSONLDStarMapper


models = {
    'oslo': OsloMapper,
    'smart_data_models': SDMMapper,
    'smart_data_models_kv': SDMMapperKV,
    'json_ld_star': JSONLDStarMapper,
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
                if self.app.config.get('SAMPLES'):
                    raw = sample(raw, self.app.config['SAMPLES'])

                for model, mapper in models.items():
                    self.data[model] = json.dumps(mapper.map_data(source, self.app.config['BASE_URI'], raw), indent=2)
            except Exception as e:
                self.app.logger.error(e)
            finally:
                self.app.logger.info('Sleeping for {}s'.format(interval))
                await asyncio.sleep(interval)
