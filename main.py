from util import *
from database import Database

db = Database("places/dc.json")


nine_am = time_to_seconds("09:00:00")
thirty_minutes = time_to_seconds("00:30:00")
college_park = db.station_id_for_name("COLLEGE PARK")

paths = db.search(college_park, nine_am, thirty_minutes)
for path in paths:
    db.print_path(path)
