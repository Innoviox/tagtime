import json
from util import Location, Station, Route, time_to_seconds
from trip import Trip
from timetable import Timetable
from search import search

json_data = json.load(open("places/dc.json"))

stations = []
routes = []
trips = []

for stop_id, station in json_data['stations'].items():
    stations.append(Station(
        name=station['name'],
        location=Location(lat=station['location']['lat'], lon=station['location']['lon']),
        stop_id=stop_id
    ))

for route in json_data['routes']:
    routes.append(Route(
        route_id=route['route_id'],
        short_name=route['route_short_name'],
        color=route['route_color']
    ))

for trip_id, trip in json_data['trips'].items():
    trips.append(Trip(
        trip_id=trip_id,
        route_id=trip['route_id'],
        headsign=trip['headsign'],
        stations=trip['stations']
    ))

timetable = Timetable(trips)

nine_am = time_to_seconds("09:00:00")
thirty_minutes = time_to_seconds("00:30:00")
college_park = [i for i in stations if "COLLEGE PARK" in i.name][0].stop_id

for path in search(college_park, nine_am, timetable, thirty_minutes):
    for station in path:
        print([i for i in stations if i.stop_id == station][0].name, end=" -> ")
    print()