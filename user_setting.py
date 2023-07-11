from tdx.bus import enum as BusEnum
from typing import Dict, Set, Tuple, List, Any
NOTIFICATION_LIMIT = 3

class UserSetting:
    def __init__(self, username: str, city: BusEnum.City, route: int, direction: BusEnum.Direction, target_stop: str, notify_range_before_target: Tuple[int, int]):
        self._username = username
        self._city = city
        self._route = route
        self._direction = direction
        self._target_stop = target_stop
        self._notify_range_before_target = notify_range_before_target
        self._notify_stop_sequences: Set[int] = set()
        self._notify_counter = 0

    @property
    def username(self) -> str:
        return self._username
    
    @property
    def city(self) -> BusEnum.City:
        return self._city
    
    @property
    def route(self) -> int:
        return self._route
    
    @property
    def direction(self) -> BusEnum.Direction:
        return self._direction
    
    @property
    def target_stop(self) -> str:
        return self._target_stop
    
    @property
    def notify_range_before_target(self) -> Tuple[int, int]:
        return self._notify_range_before_target
    
    @property
    def notify_stop_sequences(self) -> Set[int]:
        return self._notify_stop_sequences
    
    @property
    def notify_counter(self) -> int:
        return self._notify_counter
    
    def update_notify_stop_sequences(self, stops_of_route: List[Dict[str, Any]]) -> None:
        same_direction_stops = next((route for route in stops_of_route if route.get('Direction') == self.direction.value), None)
        if same_direction_stops is None:
            raise Exception("Not existed bus route.")
        target_stop_sequence = next(stop['StopSequence'] for stop in same_direction_stops['Stops'] if self.target_stop == stop["StopName"]["Zh_tw"])
        self._notify_stop_sequences = { target_stop_sequence - i for i in range(self.notify_range_before_target[0], self.notify_range_before_target[1] + 1) }

    def increment_notify_counter(self) -> None:
        self._notify_counter += 1
    
    def has_reached_notification_limit(self) -> bool:
        return self._notify_counter >= NOTIFICATION_LIMIT 
    
    def is_bus_approaching(self, direction_stop_sequence_dict:Dict[int, Set[int]]) -> bool:
        return len(direction_stop_sequence_dict[self.direction.value] & self.notify_stop_sequences) != 0
    
    def notify(self) -> None:
        print(f'{self.username}, your bus {self.route} is approaching.')