from flask import Flask, render_template, jsonify
from gevent.pywsgi import WSGIServer
from threading import Thread
from time import sleep

app = Flask(__name__)

app.template_folder = "render_templates"
app.static_folder = "static"


class Stat:
    def __init__(self, title, value, username, kit):
        self.title = title
        self.value = value
        self.username = username
        self.kit = kit


stats = [Stat("Most Kills", "65", "Recovs", "(ninja)"),
         Stat("Most Steals", "16", "TheSpartan33", "(soldier)")]


@app.route("/")
def home():
    return "Welcome to the CMS stream tool web server"


@app.route("/statscard/")
def stats_page():
    return render_template("stats_card_no_content.html")


overlay_status_dict = {
    "stats_card": {
        "status": 1,  # can be 0 = "hidden" or 1 = "showing"
        "map_info": "Map 3 - Castle Caverns"
    }
}


def toggle_stats_card():
    if overlay_status_dict["stats_card"]["status"] == 1:
        overlay_status_dict["stats_card"]["status"] = 0
        print("Hiding stats card")
    elif overlay_status_dict["stats_card"]["status"] == 0:
        overlay_status_dict["stats_card"]["status"] = 1
        print("Showing stats card")


def hide_stats_card():
    overlay_status_dict["stats_card"]["status"] = 0


def show_stats_card():
    overlay_status_dict["stats_card"]["status"] = 1


@app.route("/overlay_status", methods=["GET"])
def get_overlay_status():
    return jsonify(overlay_status_dict)


@app.route('/statscard/content/', methods=["GET"])
def stats_content():
    return render_template("stats_card_content.html", stats_for_card=stats,
                           map_info=overlay_status_dict["stats_card"]["map_info"])


def start_server_thread():
    http_server = WSGIServer(('', 5000), app, log=None)
    http_server.serve_forever()


def start_server():
    server_thread = Thread(target=start_server_thread)
    server_thread.start()

    print("Started Flask Server")









