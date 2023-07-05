import settings
from tdx_bus_api import *
from bus_tracker import BusTracker
from user_setting import UserSetting

bus_tracker = BusTracker()
setting = UserSetting(username='YuXing', city='Taipei', route=672, target_stop='博仁醫院', before_target_stop=(3, 5))
bus_tracker.subscribe_route_notification(setting)
bus_tracker.track()