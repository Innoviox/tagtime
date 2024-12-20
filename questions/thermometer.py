from database import Database


class ThermometerQuestion:
    def __init__(self, **kwargs):
        self.start = kwargs.get("start")
        self.end = kwargs.get("end")
        self.db = kwargs.get("db")

    def query(self, target: str):
        s2 = self.db.stations[target].location
        d1 = self.start.distance(s2)
        d2 = self.end.distance(s2)

        if d1 < d2:
            return -1
        return 1
