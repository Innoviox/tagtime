def search(startStation, startTime, timetable, runTime):
    possibleStations = []
    queue = [(startStation.stop_id, startTime)]
    visited = []

    while queue:
        currentStation, time = queue.pop(0)
        if currentStation in visited or time >= runTime:
            continue

        visited.append(currentStation)
        possibleStations.append(currentStation)

        for route in timetable.fromStation(currentStation, time):
            for (station, arrivalTime) in route.stations.items(): 
                queue.append((station, arrivalTime))