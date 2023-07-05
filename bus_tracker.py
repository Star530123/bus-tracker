from user_setting import UserSetting
from tdx_bus_api import *

class BusTracker:
    def __init__(self):
        self.route_subscription_dict = {}
    
    def subscribe_route_notification(self, setting: UserSetting) -> None:
        key = (setting.city, setting.route)
        if key not in self.route_subscription_dict:
            self.route_subscription_dict[key] = [setting]
        else:
            self.route_subscription_dict[key].append(setting)
    
    def track(self) -> str:
        for (city, route), value in self.route_subscription_dict.items():
            print(get_bus_real_time_near_stop(city, route))
