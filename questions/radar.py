from questions.base import BaseQuestion
from database import Database

class RadarQuestion(BaseQuestion):
    def __init__(self, **kwargs):
        self.dist = kwargs.get('dist')
        self.origin = kwargs.get('origin')

    def make_query(self, db: Database):
        s1 = db.stations[self.origin]
        def query(target: str):
            s2 = db.stations[target]
            return s1.location.distance(s2.location) <= self.dist
        return query
        