from dotenv import load_dotenv

load_dotenv()

from tdx_api.bus.v2.api import *
from bus_tracker import BusTracker
from user_setting import UserSetting
import time
import tdx_api.bus.enum as BusEnum

if __name__=='__main__':
    bus_tracker = BusTracker()
    setting = UserSetting(
        username='YuXing', 
        city=BusEnum.City.TPE.value, 
        route=672, 
        direction=BusEnum.Direction.INBOUND, 
        target_stop='博仁醫院', 
        before_target_stop=(3, 5)
    )
    setting2 = UserSetting(
        username='Simon', 
        city=BusEnum.City.TPE.value, 
        route=214, 
        direction=BusEnum.Direction.OUTBOUND, 
        target_stop='光華商場', 
        before_target_stop=(3, 7)
    )
    bus_tracker.subscribe_route_notification(setting)
    bus_tracker.subscribe_route_notification(setting2)

    while bus_tracker.user_count != 0:
        start = time.time()
        bus_tracker.track()
        end = time.time()

        print('{t} seconds/track'.format(t=end-start))
        time.sleep(5)

    print('All users have notified. Stop the program.')