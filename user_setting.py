from tdx_api.bus import enum as BusEnum
NOTIFICATION_LIMIT = 3

class UserSetting:
    def __init__(self, username, city: BusEnum.City, route, direction: BusEnum.Direction, target_stop, before_target_stop: tuple):
        self.username = username
        self.city = city
        self.route = route
        self.direction = direction
        self.target_stop = target_stop
        self.before_target_stop = before_target_stop
        self.notify_stops = {}
        self.notify_counter = 0

    # TODO refactor
    # 這部分直接封裝在 __init__ 應該比較好
    def update_information(self, stops_of_route):
        same_direction_stops = next((route for route in stops_of_route if BusEnum.Direction(route.get('Direction')) == self.direction), None)
        if same_direction_stops is None:
            raise Exception("Not existed bus route.")
        target_stop_sequence = next(stop['StopSequence'] for stop in same_direction_stops['Stops'] if self.target_stop == stop["StopName"]["Zh_tw"])
        self.notify_stops = { target_stop_sequence - i for i in range(self.before_target_stop[0], self.before_target_stop[1] + 1) }

    def increment_notify_counter(self):
        self.notify_counter += 1
    
    def has_reached_notification_limit(self):
        return self.notify_counter >= NOTIFICATION_LIMIT 