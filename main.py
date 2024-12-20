import json
from util import *
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

def name_for_station_id(station_id):
    return [i for i in stations if i.stop_id == station_id][0].name

for path in search(college_park, nine_am, timetable, thirty_minutes):
    print(name_for_station_id(path.startStation), " -> ", name_for_station_id(path.last_station()))
    prev = path.startStation
    for transfer in path.transfers:
        trip_id, station = transfer
        trip = [i for i in trips if i.trip_id == trip_id][0]
        route = [i for i in routes if i.route_id == trip.route_id][0]
        print(f"\t{route.short_name} to {trip.headsign} at {name_for_station_id(station)} / {seconds_to_time(trip.stations[prev])} - {seconds_to_time(trip.stations[station])}")
        prev = station