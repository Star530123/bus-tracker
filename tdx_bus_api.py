import requests
import json
import os

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

AUTH_URL="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
TDX_V2_BUS_API_BASE_URL = 'https://tdx.transportdata.tw/api/basic'

def get_bus_real_time_near_stop(city, route, top=30, format='JSON'):
    url = '{base_url}/v2/Bus/RealTimeNearStop/City/{city_name}/{route_name}?%24top={top}&%24format={format}'.format(
        base_url=TDX_V2_BUS_API_BASE_URL, 
        city_name=city, 
        route_name=route, 
        top=top, 
        format=format
    )
    return requests.get(url, headers=__get_api_header())

def __get_api_header():
    authentication = requests.post(AUTH_URL, __get_auth_header()).text
    access_token = json.loads(authentication).get('access_token')
    return{
        'authorization': 'Bearer '+ access_token
    }

def __get_auth_header():
    if CLIENT_ID is None or CLIENT_SECRET is None:
        raise Exception('Please set CLIENT_ID and CLIENT_SECRET!')
    content_type = 'application/x-www-form-urlencoded'
    grant_type = 'client_credentials'
    return {
        'content-type' : content_type,
        'grant_type' : grant_type,
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET
    }
