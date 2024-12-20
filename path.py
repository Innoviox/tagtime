class Path:
    def __init__(self, startStation: str, transfers = []):
        self.startStation = startStation
        self.transfers = transfers

    def add_transfer(self, trip_id, station):
        new_transfers = self.transfers + [(trip_id, station)]
        return Path(self.startStation, new_transfers)

    def last_station(self):
        if self.transfers:
            return self.transfers[-1][1]
        return self.startStation