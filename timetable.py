class Timetable:
    def __init__(self, routes):
        self.routes = routes

    def fromStation(self, station, time):
        for route in self.routes:
            if r := route.truncated(station, time):
                yield r