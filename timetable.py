class Timetable:
    def __init__(self, trips):
        self.trips = trips

    def fromStation(self, station, time):
        for trip in self.trips.values():
            if r := trip.truncated(station, time):
                yield r