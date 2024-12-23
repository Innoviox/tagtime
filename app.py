from flask import Flask, render_template_string
from map import Map
from database import Database
from game import Game
from util import *

app = Flask(__name__)
map = Map()
map.load_routes(
    "transitland/f-dqc-wmata~rail-17682fd6de41fac6919edc1f433c8fc1f4aab3a8/shapes.txt"
)
map.set_db(Database("places/dc.json"))
map.draw_routes()
map.draw_stations()

game = Game(map.db, "COLLEGE PARK", 9 * 60 * 60, 30 * 60)


@app.route("/")
def fullscreen():
    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                <script>
                    async function get_url(url) {
                        console.log(await fetch(url));
                    }
                </script>
                </head>
                <body>
                    <h1>{{ seconds_to_time(game.start_time + game.total_time) }}</h1>
                    <div style="flex: 1; display: flex">
                        <button onclick="get_url('/test')">Test</button>
                    </div>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        seconds_to_time=seconds_to_time,
        game=game,
        iframe=map.iframe,
    )

@app.route("/test")
def test():
    print("test!")
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
