class Trip:
    def __init__(self, trip_id, route_id, headsign, stations: dict[str, int]):
        # stations is a dictionary of station objects and their arrival times
        # time is measured (as always) as seconds since midnight

        self.trip_id = trip_id
        self.route_id = route_id
        self.headsign = headsign
        self.stations = stations

    def truncated(self, station: str, time: int):
        if station not in self.stations:
            return None

        truncatedRoute = Trip(self.trip_id, self.route_id, self.headsign, {})
        found = False
        for s, t in self.stations.items():
            if s == station and t >= time:
                found = True
            if found:
                truncatedRoute.stations[s] = t

        return truncatedRoute if found else None
