import requests
import json
import os
import time

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

AUTH_URL="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
TDX_V2_BUS_API_BASE_URL = 'https://tdx.transportdata.tw/api/basic'

api_header_data = {}

def __api_url(api_endpoint: str, query: str) -> str:
    return '{base_url}{api_endpoint}?{query}'.format(
        base_url=TDX_V2_BUS_API_BASE_URL,
        api_endpoint=api_endpoint,
        query=query
    )

# TODO refactor
# 1. GET bus 相關 API 可以在extract邏輯，再想一下要抽共用method還是抽成class
# 2. __format_query 再思考一下有沒有更好的寫法以及用法，像是select和filter能夠更方便使用 (像是filter的odata語法可抽成enum)
def get_bus_real_time_near_stop(city, route, top=30, format='JSON', select='PlateNumb,Direction,StopName', filter=None) -> str:
    api_endpoint = '/v2/Bus/RealTimeNearStop/City/{city_name}/{route_name}'.format(city_name=city, route_name=route)
    url = __api_url(api_endpoint=api_endpoint, query=__format_query(top=top, format=format, select=select, filter=filter))
    return json.loads(requests.get(url, headers=__get_api_header()).text)

def get_bus_stop_of_route(city, route, top=30, format='JSON', select='Direction,Stops', filter=None) -> str:
    api_endpoint = '/v2/Bus/StopOfRoute/City/{city_name}/{route_name}'.format(city_name=city, route_name=route)
    url = __api_url(api_endpoint=api_endpoint, query=__format_query(top=top, format=format, select=select, filter=filter))
    return json.loads(requests.get(url, headers=__get_api_header()).text)

def __get_api_header() -> dict:
    if len(api_header_data) == 0 or time.time() >= api_header_data['expired_time']:
        authentication = requests.post(AUTH_URL, __get_auth_header()).text
        response = json.loads(authentication)
        api_header_data['api_header'] = {
            'authorization': 'Bearer '+ response.get('access_token')
        }
        api_header_data['expired_time'] = time.time() + response.get('expires_in')
        print(api_header_data)
    return api_header_data['api_header'] 

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
