from timetable import Timetable

def search(startStation: str, startTime: int, timetable: Timetable, runTime: int):
    possibleStations = []
    queue = [(startStation, startTime)]
    visited = {}

    while queue:
        # print(queue)
        # input()
        currentStation, time = queue.pop(0)
        if currentStation in visited or time > startTime + runTime:
            continue

        visited[currentStation] = True
        possibleStations.append(currentStation)

        for route in timetable.fromStation(currentStation, time):
            for (station, arrivalTime) in route.stations.items(): 
                if station not in visited and arrivalTime <= startTime + runTime:
                    queue.append((station, arrivalTime))

    return possibleStations