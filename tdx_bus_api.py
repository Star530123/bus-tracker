import requests
import json
import os

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

AUTH_URL="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
TDX_V2_BUS_API_BASE_URL = 'https://tdx.transportdata.tw/api/basic'

def get_bus_real_time_near_stop(city, route, top=30, format='JSON') -> str:
    url = '{base_url}/v2/Bus/RealTimeNearStop/City/{city_name}/{route_name}?%24top={top}&%24format={format}&%24select={select}'.format(
        base_url=TDX_V2_BUS_API_BASE_URL, 
        city_name=city, 
        route_name=route, 
        top=top, 
        format=format,
        select=__column_select()
    )
    return requests.get(url, headers=__get_api_header()).text

def get_bus_stop_of_route(city, route, top=30, format='JSON') -> str:
    url = '{base_url}/v2/Bus/StopOfRoute/City/{city_name}/{route_name}?%24top={top}&%24format={format}&%24select={select}'.format(
        base_url=TDX_V2_BUS_API_BASE_URL, 
        city_name=city, 
        route_name=route, 
        top=top, 
        format=format,
        select=__column_select()
    )
    return requests.get(url, headers=__get_api_header())

def __get_api_header() -> dict:
    # TODO 需要修改取得 access_token 的時間點，每次打api都要重新取得access_token太浪費資源
    # https://github.com/tdxmotc/SampleCode
    authentication = requests.post(AUTH_URL, __get_auth_header()).text
    access_token = json.loads(authentication).get('access_token')
    return{
        'authorization': 'Bearer '+ access_token
    }

def __get_auth_header() -> dict:
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

def __column_select(columns:list =['PlateNumb', 'Direction', 'StopName']) -> str:
    separator = ','
    return separator.join(column for column in columns)