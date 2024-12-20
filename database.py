import json, collections
import tqdm
from util import *
from trip import Trip
from timetable import Timetable
from path import Path
from questions import *


class Database:
    def __init__(self, path):
        self.stations = {}
        self.routes = {}
        self.trips = {}

        json_data = json.load(open(path))

        for stop_id, station in json_data["stations"].items():
            self.stations[stop_id] = Station(
                name=station["name"],
                location=Location(
                    lat=station["location"]["lat"], lon=station["location"]["lon"]
                ),
                stop_id=stop_id,
            )

        for route in json_data["routes"]:
            self.routes[route["route_id"]] = Route(
                route_id=route["route_id"],
                short_name=route["route_short_name"],
                color=route["route_color"],
            )

        for trip_id, trip in json_data["trips"].items():
            self.trips[trip_id] = Trip(
                trip_id=trip_id,
                route_id=trip["route_id"],
                headsign=trip["headsign"],
                stations=trip["stations"],
            )

        self.timetable = Timetable(self.trips)

    def name_for_station_id(self, station_id):
        return self.stations[station_id].name

    def station_for_name(self, name):
        for station in self.stations.values():
            if name in station.name:
                return station

    def print_path(self, path):
        print(
            self.name_for_station_id(path.startStation),
            " -> ",
            self.name_for_station_id(path.last_station()),
        )
        prev = path.startStation
        for transfer in path.transfers:
            trip_id, station = transfer
            trip = self.trips[trip_id]
            route = self.routes[trip.route_id]
            print(
                f"\t{route.short_name} to {trip.headsign} at {self.name_for_station_id(station)} / {seconds_to_time(trip.stations[prev])} - {seconds_to_time(trip.stations[station])}"
            )
            prev = station

    def search(self, startStation: str, startTime: int, runTime: int):
        possibleStations = []
        queue = [(Path(startStation), startTime)]
        visited = {}

        while queue:
            path, time = queue.pop(0)
            last_station = path.last_station()
            if last_station in visited or time > startTime + runTime:
                continue

            visited[last_station] = True
            possibleStations.append(path)

            for trip in self.timetable.fromStation(last_station, time):
                for station, arrivalTime in trip.stations.items():
                    if station not in visited and arrivalTime <= startTime + runTime:
                        new_path = path.add_transfer(trip.trip_id, station)
                        queue.append((new_path, arrivalTime))

        return possibleStations

    def get_end_time(self, path, start_time):
        if not path.transfers:
            return start_time
        trip = self.trips[path.transfers[-1][0]]
        return trip.stations[path.last_station()]

    def make_all_questions(self, origin: str, start_time: int):
        questions = []
        radars = {}
        thermometers = collections.defaultdict(dict)
        # cap thermometers at 30 minutes
        # todo: walking thermometers?
        for path in tqdm.tqdm(self.search(origin, start_time, 30 * 60)):
            stations = list(self.all_stations(path, start_time))
            for i, (station, time) in enumerate(stations):
                for dist in [0.5, 1, 2, 3, 4, 5]:  # todo custom radar
                    if station not in radars:
                        radars[station] = True
                        questions.append(
                            RadarQuestion(
                                dist=dist,
                                origin=station,
                                db=self,
                                time=time - start_time,
                            )
                        )

                for end, end_time in stations[i + 1 :]:
                    if end not in thermometers[station]:
                        thermometers[station][end] = True
                        questions.append(
                            ThermometerQuestion(
                                start=station,
                                end=end,
                                db=self,
                                time=end_time - start_time,
                            )
                        )
        return questions

    def rate_question(self, question, paths):
        return sum(1 for path in paths if question.query(path.last_station()))

    def all_stations(self, path, start_time):
        yield path.startStation, start_time
        for i, (trip_id, station) in enumerate(path.transfers):
            switch_station = None
            if i < len(path.transfers) - 1:
                switch_station = path.transfers[i + 1][1]
            trip = self.trips[trip_id]
            on = False
            for s, t in trip.stations.items():
                if s == station:
                    on = True
                if on:
                    yield s, t
                if switch_station and s == switch_station:
                    break
