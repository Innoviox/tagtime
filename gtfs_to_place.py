import csv, json

class GTFSParser:
    def __init__(self, path, station_key, name_strip):
        self.base_path = path
        self.station_key = station_key
        self.name_strip = name_strip
        
        self.stations = {}
        self.routes = []
        self.trips = {}

    def parse_stations(self):
        self.stations = {}
        with open(f"{self.base_path}/stops.txt") as f:
            reader = csv.DictReader(f)
            for row in reader:
                stop_id = row['stop_id']
                if stop_id.startswith(self.station_key):
                    name = row['stop_name']#.strip(self.name_strip)
                    location = {'lat': row['stop_lat'], 'lon': row['stop_lon']}
                    self.stations[stop_id] = {
                        'name': name, 
                        'location': location,
                        'children': []
                    }
                else:
                    self.stations[row['parent_station']]['children'].append(stop_id)

    def parse_routes(self):
        self.routes = []
        with open(f"{self.base_path}/routes.txt") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.routes.append({
                    'route_id': row['route_id'],
                    'route_short_name': row['route_short_name'],
                    'route_color': row['route_color']
                })

    def parse_trips(self):
        self.trips = {}
        with open(f"{self.base_path}/trips.txt") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.trips[row['trip_id']] = {
                    'route_id': row['route_id'],
                    'headsign': row['trip_headsign'],
                    'timetable': []
                }

        with open(f"{self.base_path}/stop_times.txt") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.trips[row['trip_id']]['timetable'].append({
                    'stop_id': row['stop_id'],
                    'arrival_time': row['arrival_time']
                })

    def to_json(self):
        self.parse_stations()
        self.parse_routes()
        self.parse_trips()

        return json.dumps({
            'stations': self.stations,
            'routes': self.routes,
            'trips': self.trips
        })

if __name__ == '__main__':
    open("places/dc.json", "w").write(GTFSParser("transitland/f-dqc-wmata~rail-17682fd6de41fac6919edc1f433c8fc1f4aab3a8", "STN", "METRORAIL STATION").to_json())