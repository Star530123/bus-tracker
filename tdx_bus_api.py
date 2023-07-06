import requests
import json
import os

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

AUTH_URL="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
TDX_V2_BUS_API_BASE_URL = 'https://tdx.transportdata.tw/api/basic'

def __api_url(api_endpoint: str, query: str) -> str:
    return '{base_url}{api_endpoint}?{query}'.format(
        base_url=TDX_V2_BUS_API_BASE_URL,
        api_endpoint=api_endpoint,
        query=query
    )

def get_bus_real_time_near_stop(city, route, top=30, format='JSON', select='PlateNumb,Direction,StopName', filter=None) -> str:
    api_endpoint = '/v2/Bus/RealTimeNearStop/City/{city_name}/{route_name}'.format(city_name=city, route_name=route)
    url = __api_url(api_endpoint=api_endpoint, query=__format_query(top=top, format=format, select=select, filter=filter))
    return requests.get(url, headers=__get_api_header()).text

def get_bus_stop_of_route(city, route, top=30, format='JSON', select='PlateNumb,Direction,StopName', filter=None) -> str:
    api_endpoint = '/v2/Bus/StopOfRoute/City/{city_name}/{route_name}'.format(city_name=city, route_name=route)
    url = __api_url(api_endpoint=api_endpoint, query=__format_query(top=top, format=format, select=select, filter=filter))
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

def __format_query(**queries) -> str:
    queries = {k: v for k, v in queries.items() if v is not None}
    query_list = ['${k}={v}'.format(k=k, v=v) for k, v in queries.items()]
    return '&'.join(query_list)
