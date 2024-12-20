from questions.base import BaseQuestion


class RadarQuestion(BaseQuestion):
    def __init__(self, **kwargs):
        self.dist = kwargs.get("dist")
        self.origin = kwargs.get("origin")
        self.db = kwargs.get("db")
        self.time = kwargs.get("time")

    def query(self, target: str):
        s1 = self.db.stations[self.origin]
        s2 = self.db.stations[target]
        return s1.location.distance(s2.location) <= self.dist

    def __str__(self):
        return f"RadarQuestion: {self.dist}mi ({self.time}s)"
