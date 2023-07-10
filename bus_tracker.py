from user_setting import UserSetting
import tdx.bus.v2.api as bus_api
from tdx.bus import *
from typing import Dict, Tuple, Set, Any, List
from itertools import groupby

class BusTracker:
    def __init__(self):
        self._route_subscription_dict: Dict[Tuple[str, int], List[UserSetting]] = {}
        self._stops_of_route_dict: Dict[Tuple[str, int], List[Dict[str, Any]]]   = {}
        self._user_count = 0
    
    @property
    def route_subscription_dict(self) -> Dict[Tuple[str, int], List[UserSetting]]:
        return self._route_subscription_dict

    @property
    def stops_of_route_dict(self) -> Dict[Tuple[str, int], List[Dict[str, Any]]]:
        return self._stops_of_route_dict
    
    @property
    def user_count(self) -> int:
        return self._user_count
    
    def _decrement_user_count(self) -> None:
        self._user_count -= 1

    def _increment_user_count(self) -> None:
        self._user_count += 1
    
    def subscribe_route_notification(self, setting: UserSetting) -> None:
        key = (setting.city, setting.route)
        setting.update_notify_stops(self._get_stops_of_route(key))
        if key not in self.route_subscription_dict:
            self.route_subscription_dict[key] = [setting]
        else:
            self.route_subscription_dict[key].append(setting)
        self._increment_user_count()
    
    def _get_stops_of_route(self, key: Tuple[str, int]) -> List[Dict[str, Any]]:
        if self.stops_of_route_dict.get(key) is not None:
            return self.stops_of_route_dict[key]
        query = Query()
        query.select([StopOfRoute.DIRECTION, StopOfRoute.STOPS])
        query.filter(f"RouteName/Zh_tw eq '{key[1]}'")
        self.stops_of_route_dict[key] = bus_api.get_bus_stop_of_route(city=key[0], route=key[1], query=query.complete())
        return self.stops_of_route_dict[key]
    
    def track(self) -> None:
        remove_set = set()
        for (city, route), user_setting_list in self.route_subscription_dict.items():
            query = Query()
            query.select([RealTimeNearStop.PLATE_NUMB, RealTimeNearStop.DIRECTION, RealTimeNearStop.STOP_NAME])
            real_time_near_stops = bus_api.get_bus_real_time_near_stop(city, route, query.complete())
            direction_stop_sequence_dict = self._direction_stop_sequence_dict(real_time_near_stops)
            print(f'[route = {route}]Current buses positions: {direction_stop_sequence_dict}')

            for user_setting in user_setting_list:
                if user_setting.is_bus_approaching(direction_stop_sequence_dict):
                    user_setting.notify()
                    user_setting.increment_notify_counter()
                    if user_setting.has_reached_notification_limit():
                        remove_set.add(user_setting)
                        self._decrement_user_count()

        remove_key_list = []
        for key, user_setting_list in self.route_subscription_dict.items():
            self.route_subscription_dict[key] = [setting for setting in user_setting_list if setting not in remove_set]
            if len(user_setting_list) == 0:
                remove_key_list.append(key) 

        for remove_key in remove_key_list:
            del self.route_subscription_dict[remove_key]
            del self.stops_of_route_dict[remove_key]

    def _direction_stop_sequence_dict(self, real_time_near_stops: List[Dict[str, Any]]) -> Dict[int, Set[int]]:
        sorted_stops = sorted(real_time_near_stops, key=lambda stop: stop['Direction'])
        grouped_stops = groupby(sorted_stops, lambda stop: stop['Direction'])
        
        return {direction: set(map(lambda stop: stop['StopSequence'], stops)) for direction, stops in grouped_stops}
