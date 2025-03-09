import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"


def get_static_api_image(ll, z, theme, flag=False):
    map_api_server = 'https://static-maps.yandex.ru/v1?'
    map_params = {
        'll': ','.join(map(str, ll)),
        'apikey': API_KEY,
        'theme': theme,
        'z': z,
        'pt': "~".join(["{0},pm2dgl".format(','.join(map(str, ll)) if flag else '0,0')])
    }
    session = requests.Session()
    retry = Retry(total=10, connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    response = session.get(map_api_server, params=map_params)
    if response:
        return response.content
    else:
        raise RuntimeError('Ошибка выполнения запроса.')