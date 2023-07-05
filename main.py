import settings
from tdx_bus_api import *

print(get_bus_real_time_near_stop('Taipei', 672).text)