from flask import Flask, render_template, jsonify
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

app.template_folder = "render_templates"


class Stat:
    def __init__(self, title, value, username, kit):
        self.title = title
        self.value = value
        self.username = username
        self.kit = kit


stats = [Stat("Most Kills", "65", "b0squet", "archer")]


@app.route("/")
def hello_world():
    return "Welcome to the CMS stream tool web server"


@app.route("/statscard/")
def stats_page():
    return "The stats page"


overlay_status_dict = {
    "stats_card": {
        "status": "showing"  # can be "hidden" or "showing"
    }
}


@app.route("/overlay_status", methods=["GET"])
def get_overlay_status():
    return jsonify(overlay_status_dict)


@app.route('/statscard/content/', methods=["GET"])
def stats_content():
    return render_template("stats_card_content.html", stats_for_card=stats, map_info="Map 1 - Adrenaline I")


if __name__ == '__main__':
    # Debug/Development
    app.run(host="localhost", port=5000, debug=False)

    """
    # Production
    http_server = WSGIServer(('', 5000), app, log=None)
    http_server.serve_forever()

    import logging

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    """






