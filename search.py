from timetable import Timetable
from path import Path

def search(startStation: str, startTime: int, timetable: Timetable, runTime: int):
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

        for trip in timetable.fromStation(last_station, time):
            for (station, arrivalTime) in trip.stations.items(): 
                if station not in visited and arrivalTime <= startTime + runTime:
                    new_path = path.add_transfer(trip.trip_id, station)
                    queue.append((new_path, arrivalTime))

    return possibleStations