from user_setting import UserSetting
from tdx_bus_api import *
from typing import Dict, Tuple
from tdx_api.bus.response import *

class BusTracker:
    def __init__(self):
        self._route_subscription_dict = {}
        self._stops_of_route_dict: dict[tuple, UserSetting]  = {}
        self._user_count = 0
    
    @property
    def route_subscription_dict(self) -> Dict[Tuple, UserSetting]:
        return self._route_subscription_dict

    @property
    def stops_of_route_dict(self):
        return self._stops_of_route_dict
    
    @property
    def user_count(self) -> int:
        return self._user_count
    
    def decrement_user_count(self) -> None:
        self._user_count -= 1

    def increment_user_count(self) -> None:
        self._user_count += 1
    
    def get_stops_of_route(self, key, query):
        if self.stops_of_route_dict.get(key) is not None:
            return self.stops_of_route_dict[key]
        self.stops_of_route_dict[key] = get_bus_stop_of_route(city=key[0], route=key[1], query=query)
        return self.stops_of_route_dict[key]

    def subscribe_route_notification(self, setting: UserSetting) -> None:
        key = (setting.city, setting.route)
        filter = 'SubRouteName/Zh_tw eq \'{route}\''.format(route=setting.route)
        query = Query()
        query.select([StopOfRoute.DIRECTION, StopOfRoute.STOPS])
        query.filter(filter)
        stops_of_route = self.get_stops_of_route(key, query.complete())
        setting.update_information(stops_of_route)
        if key not in self.route_subscription_dict:
            self.route_subscription_dict[key] = [setting]
        else:
            self.route_subscription_dict[key].append(setting)
        self.increment_user_count()
    
    def track(self) -> None:
        # 總User數量為N，總公車數量為M
        # 雖然是兩層for迴圈，但時間複雜度僅有 O(M+N)
        # TODO refactor
        # 1. Readability, notify & 處理不同方向路線的邏輯或許可以再拆成其他method
        # 2. Notify logic(Responsibility), 現在通知邏輯是寫在 bus_tracker 中且直接print，不過完整版應該是要通知到"個別使用者"，所以通知邏輯應該要寫在UserSetting，或者將要通知的使用者從bus_tracker回傳出去
        remove_set = set()
        for (city, route), user_setting_list in self.route_subscription_dict.items():
            query = Query()
            query.select([RealTimeNearStop.PLATE_NUMB, RealTimeNearStop.DIRECTION, RealTimeNearStop.STOP_NAME])
            real_time_near_stops = get_bus_real_time_near_stop(city, route, query.complete())
            direction_real_time_stop_sequence_dict = {}
            for real_time_near_stop in real_time_near_stops:
                direction = real_time_near_stop['Direction']
                if direction_real_time_stop_sequence_dict.get(direction) is None:
                    direction_real_time_stop_sequence_dict[direction] = set()
                direction_real_time_stop_sequence_dict[direction].add(real_time_near_stop['StopSequence'])
            print('Current buses positions: {stops}'.format(stops=direction_real_time_stop_sequence_dict))
            for user_setting in user_setting_list:
                if len(direction_real_time_stop_sequence_dict[user_setting.direction.value] & user_setting.notify_stops) != 0:
                    message = '{username}, your bus {route} is approaching.'.format(
                        username=user_setting.username, 
                        route=user_setting.route
                    )
                    print(message)
                    user_setting.increment_notify_counter()
                    if user_setting.has_reached_notification_limit():
                        remove_set.add(user_setting)
                        self.decrement_user_count()
        for key, user_setting_list in self.route_subscription_dict.items():
            self.route_subscription_dict[key] = [setting for setting in user_setting_list if setting not in remove_set]