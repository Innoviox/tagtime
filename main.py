from util import *
from database import Database
from questions import RadarQuestion

db = Database("places/dc.json")


nine_am = time_to_seconds("09:00:00")
thirty_minutes = time_to_seconds("00:30:00")
college_park = db.station_for_name("COLLEGE PARK").stop_id

paths = db.search(college_park, nine_am, thirty_minutes)
for path in paths:
    db.print_path(path)

for radar_dist in range(1, 11):
    print(f"Radar distance: {radar_dist}")
    radar = RadarQuestion(dist=radar_dist, origin=college_park)
    i, j = 0, 0
    for path in paths:
        if radar.make_query(db)(path.last_station()):
            i += 1
        j += 1
    print(f"Total: {i}/{j}")
