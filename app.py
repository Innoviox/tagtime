from flask import Flask, render_template_string
from map import Map
from database import Database

app = Flask(__name__)
map = Map()
map.load_routes("transitland/f-dqc-wmata~rail-17682fd6de41fac6919edc1f433c8fc1f4aab3a8/shapes.txt")
map.set_db(Database("places/dc.json"))
map.draw_routes()

@app.route("/")
def fullscreen():
    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Using an iframe</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=map.iframe,
    )


if __name__ == "__main__":
    app.run(debug=True)