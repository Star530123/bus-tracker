class UserSetting:

    def __init__(self, username, city, route, target_stop, before_target_stop: tuple):
        self.username = username
        self.city = city
        self.route = route
        self.target_stop = target_stop
        self.before_target_stop = before_target_stop