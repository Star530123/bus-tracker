from enum import Enum

class RealTimeNearStop(Enum):
    PLATE_NUMB = 'PlateNumb'
    DIRECTION = 'Direction'
    STOP_NAME = 'StopName'

class StopOfRoute(Enum):
    DIRECTION = 'Direction'
    STOPS = 'Stops'