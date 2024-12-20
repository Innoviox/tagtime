from util import *
from database import Database

db = Database("places/dc.json")


nine_am = time_to_seconds("09:00:00")
thirty_minutes = time_to_seconds("00:30:00")
college_park = db.station_for_name("COLLEGE PARK").stop_id

paths = db.search(college_park, nine_am, thirty_minutes)
for path in paths:
    db.print_path(path)


# for radar_dist in range(1, 11):
for question in db.make_all_questions(college_park, time_to_seconds("09:30:00")):
    print(f"{question}: {db.rate_question(question, paths)}/{len(paths)}")
