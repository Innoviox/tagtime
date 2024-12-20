from timetable import Timetable

def search(startStation: str, startTime: int, timetable: Timetable, runTime: int):
    possibleStations = []
    queue = [([startStation], startTime)]
    visited = {}

    while queue:
        path, time = queue.pop(0)
        if path[-1] in visited or time > startTime + runTime:
            continue

        visited[path[-1]] = True
        possibleStations.append(path)

        for route in timetable.fromStation(path[-1], time):
            for (station, arrivalTime) in route.stations.items(): 
                if station not in visited and arrivalTime <= startTime + runTime:
                    queue.append((path + [station], arrivalTime))

    return possibleStations