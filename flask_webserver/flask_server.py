from flask import Flask, render_template, request, jsonify
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
    return render_template("stats_card/stats_card_no_content.html")


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
    return render_template("stats_card/stats_card_content.html", stats_for_card=stats,
                           map_info=overlay_status_dict["stats_card"]["map_info"])


title_screen_dict = {
    "large_text": "Large Text",
    "medium_text": "Medium Text",
    "small_text_1": "Small Text One",
    "small_text_2": "Small Text Two"
}


@app.route("/title_screen/", methods=["GET"])
def title_screen():
    if request.args.get("video") == "true":
        # http://localhost:5000/title_screen/?video=true
        # displays the video located in static/video.mp4 in the background
        return render_template("title_screen/title_with_video.html")
    else:
        return render_template("title_screen/title.html")


@app.route("/title_screen/data/", methods=["GET"])
def title_screen_data_api():
    return jsonify(title_screen_dict)


def start_server_thread():
    http_server = WSGIServer(('', 5000), app, log=None)
    http_server.serve_forever()


def start_server():
    server_thread = Thread(target=start_server_thread)
    server_thread.start()

    print("Started Flask Server")









