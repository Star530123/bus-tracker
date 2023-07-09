from user_setting import UserSetting
from tdx_api.bus.v2.api import *
from typing import Dict, Tuple, Set
from tdx_api.bus.response import *
from itertools import groupby

class BusTracker:
    def __init__(self):
        self._route_subscription_dict = {}
        self._stops_of_route_dict: Dict[tuple, list[UserSetting]]  = {}
        self._user_count = 0
    
    @property
    def route_subscription_dict(self) -> Dict[Tuple, List[UserSetting]]:
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
    
    def subscribe_route_notification(self, setting: UserSetting) -> None:
        key = (setting.city, setting.route)
        setting.update_notify_stops(self._get_stops_of_route(key))
        if key not in self.route_subscription_dict:
            self.route_subscription_dict[key] = [setting]
        else:
            self.route_subscription_dict[key].append(setting)
        self.increment_user_count()
    
    def _get_stops_of_route(self, key):
        if self.stops_of_route_dict.get(key) is not None:
            return self.stops_of_route_dict[key]
        query = Query()
        query.select([StopOfRoute.DIRECTION, StopOfRoute.STOPS])
        query.filter(f"RouteName/Zh_tw eq '{key[1]}'")
        self.stops_of_route_dict[key] = get_bus_stop_of_route(city=key[0], route=key[1], query=query.complete())
        return self.stops_of_route_dict[key]
    
    def track(self) -> None:
        remove_set = set()
        for (city, route), user_setting_list in self.route_subscription_dict.items():
            query = Query()
            query.select([RealTimeNearStop.PLATE_NUMB, RealTimeNearStop.DIRECTION, RealTimeNearStop.STOP_NAME])
            real_time_near_stops = get_bus_real_time_near_stop(city, route, query.complete())
            direction_stop_sequence_dict = self._direction_stop_sequence_dict(real_time_near_stops)
            print(f'Current buses positions: {direction_stop_sequence_dict}')

            for user_setting in user_setting_list:
                if user_setting.is_bus_approaching(direction_stop_sequence_dict):
                    user_setting.notify()
                    user_setting.increment_notify_counter()
                    if user_setting.has_reached_notification_limit():
                        remove_set.add(user_setting)
                        self.decrement_user_count()

        for key, user_setting_list in self.route_subscription_dict.items():
            self.route_subscription_dict[key] = [setting for setting in user_setting_list if setting not in remove_set]

    def _direction_stop_sequence_dict(self, real_time_near_stops) -> Dict[int, Set[int]]:
        sorted_stops = sorted(real_time_near_stops, key=lambda stop: stop['Direction'])
        grouped_stops = groupby(sorted_stops, lambda stop: stop['Direction'])
        
        return {k: set(map(lambda stop: stop['StopSequence'], v)) for k, v in grouped_stops}
