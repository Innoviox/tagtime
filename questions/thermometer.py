from database import Database

class ThermometerQuestion:
    def __init__(self, **kwargs):
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')

    def make_query(self, db: Database):
        def query(target: str):
            s2 = db.stations[target].location
            return self.thermometer(self.start, self.end, s2)
        return query

    def thermometer(self, start, end, target):
        d1 = start.distance(target)
        d2 = end.distance(target)

        if d1 < d2:
            return -1
        return 1