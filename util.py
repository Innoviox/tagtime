from geopy import distance


class Location:
    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    def distance(self, to):
        return distance.distance(
            (self.latitude, self.longitude), (to.latitude, to.longitude)
        ).miles

    def __str__(self):
        return f"Location({self.latitude}, {self.longitude})"


class Station:
    def __init__(self, name, location, stop_id):
        self.name = name
        self.location = location
        self.stop_id = stop_id


class Route:
    def __init__(self, route_id, short_name, color):
        self.route_id = route_id
        self.short_name = short_name
        self.color = color


def time_to_seconds(time):
    h, m, s = map(int, time.split(":"))
    return h * 60 * 60 + m * 60 + s


def seconds_to_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"
