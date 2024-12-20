from questions.base import BaseQuestion


class RadarQuestion(BaseQuestion):
    def __init__(self, **kwargs):
        self.dist = kwargs.get("dist")
        self.db = kwargs.get("db")
        self.origin = self.db.stations[kwargs.get("origin")]
        self.time = kwargs.get("time")

    def query(self, target: str):
        s2 = self.db.stations[target]
        return self.origin.location.distance(s2.location) <= self.dist

    def __str__(self):
        return f"RadarQuestion from {self.origin.name}: {self.dist}mi ({self.time}s)"
