class Route:
    def __init__(self, stations):
        # stations is a dictionary of station objects and their arrival times
        self.stations = stations

    def truncated(self, station, time):
        if station not in self.stations:
            return None

        truncatedRoute = Route({})
        found = False
        for (s, t) in self.stations.items():
            if s.stop_id == station.stop_id and t >= time:
                found = True
            if found:
                truncatedRoute.stations[s] = t

        return truncatedRoute if found else None