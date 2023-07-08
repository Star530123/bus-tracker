import settings
from tdx_bus_api import *
from bus_tracker import BusTracker
from user_setting import UserSetting
import time
import tdx_api.bus.enum as BusEnum

bus_tracker = BusTracker()
setting = UserSetting(
    username='YuXing', 
    city=BusEnum.City.TPE.value, 
    route=672, 
    direction=BusEnum.Direction.INBOUND, 
    target_stop='博仁醫院', 
    before_target_stop=(3, 5)
)
bus_tracker.subscribe_route_notification(setting)

while bus_tracker.user_count != 0:
    start = time.time()
    bus_tracker.track()
    end = time.time()

    print('{t} seconds/track'.format(t=end-start))
    time.sleep(5)

print('All users have notified. Stop the program.')