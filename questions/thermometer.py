class ThermometerQuestion:
    def __init__(self, **kwargs):
        self.db = kwargs.get("db")
        self.time = kwargs.get("time")

        self.start = self.db.stations[kwargs.get("start")]
        self.end = self.db.stations[kwargs.get("end")]

    def query(self, target: str):
        s2 = self.db.stations[target].location
        d1 = self.start.location.distance(s2)
        d2 = self.end.location.distance(s2)

        if d1 < d2:
            return 0
        return 1

    def __str__(self):
        return (
            f"ThermometerQuestion: {self.start.name} -> {self.end.name} ({self.time}s)"
        )
