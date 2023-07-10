import requests
import json
import os
import time
from tdx_api.bus.query import *

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

AUTH_URL="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
TDX_V2_BUS_API_BASE_URL = 'https://tdx.transportdata.tw/api/basic'

api_header_data: Dict[Any] = {}

def get_bus_real_time_near_stop(city: str, route: int, query: str) -> List[Dict[Any]]:
    api_endpoint = '/v2/Bus/RealTimeNearStop/City/{city_name}/{route_name}'.format(city_name=city, route_name=route)
    return _get_api(api_endpoint=api_endpoint, query=query)

def get_bus_stop_of_route(city: str, route: int, query: str) -> List[Dict[Any]]:
    api_endpoint = '/v2/Bus/StopOfRoute/City/{city_name}/{route_name}'.format(city_name=city, route_name=route)
    return _get_api(api_endpoint=api_endpoint, query=query)

def _get_api(api_endpoint: str, query: str) -> Any:
    url = '{base_url}{api_endpoint}?{query}'.format(
        base_url=TDX_V2_BUS_API_BASE_URL,
        api_endpoint=api_endpoint,
        query=query
    )
    return json.loads(requests.get(url, headers=_api_header()).text)

def _api_header() -> Dict[Any]:
    if len(api_header_data) == 0 or time.time() >= api_header_data['expired_time']:
        authentication = requests.post(AUTH_URL, _auth_api_header()).text
        response: Dict[Any] = json.loads(authentication)
        api_header_data['api_header'] = {
            'authorization': 'Bearer '+ response.get('access_token')
        }
        api_header_data['expired_time'] = time.time() + response.get('expires_in')

    return api_header_data['api_header'] 

def _auth_api_header() -> Dict[Any]:
    if CLIENT_ID is None or CLIENT_SECRET is None:
        raise Exception('Please set CLIENT_ID and CLIENT_SECRET!')
    return {
        'content-type' : 'application/x-www-form-urlencoded',
        'grant_type' : 'client_credentials',
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET
    }