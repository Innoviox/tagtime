from util import *
from database import Database
from game import Game

db = Database("places/dc.json")


nine_am = time_to_seconds("09:00:00")
thirty_minutes = time_to_seconds("00:30:00")
college_park = db.station_for_name("COLLEGE PARK").stop_id

game = Game(db, college_park, nine_am, thirty_minutes)
game.play()
