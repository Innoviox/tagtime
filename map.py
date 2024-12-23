import folium
import csv
import collections


class Map:
    def __init__(self):
        self.map = folium.Map(location=[38.889805, -77.009056])
        self.map.get_root().width = "800px"
        self.map.get_root().height = "600px"

        self.routes = None
        self.db = None

    def load_routes(self, shapesfile):
        self.routes = collections.defaultdict(list)
        with open(shapesfile) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.routes[row["shape_id"]].append(
                    (row["shape_pt_lat"], row["shape_pt_lon"])
                )

    def set_db(self, db):
        self.db = db

    def draw_routes(self):
        for route_id, route_points in self.routes.items():
            color = None
            for k, v in self.db.routes.items():
                # todo make this better
                if k[0] in route_id and k != "SHUTTLE":
                    color = v.color
                    if k[0] == "S":
                        break
            if color:
                fg = folium.FeatureGroup(name=route_id)
                route = [(float(lat), float(lon)) for lat, lon in route_points]
                fg.add_child(folium.PolyLine(route, color=f"#{color}"))
                self.map.add_child(fg)

    def draw_stations(self):
        for station in self.db.stations.values():
            folium.Marker(
                location=[station.location.latitude, station.location.longitude],
                popup=station.name,
                # dot div icon
                icon=folium.DivIcon(
                    html=f"""
            <div><svg>
                <circle cx="5" cy="5" r="5" fill="#000000" />
            </svg></div>"""
                ),
            ).add_to(self.map)

    @property
    def iframe(self):
        return self.map.get_root()._repr_html_()
