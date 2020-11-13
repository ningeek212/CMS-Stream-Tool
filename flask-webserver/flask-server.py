from flask import Flask, render_template
app = Flask(__name__)

app.template_folder = "render_templates"

@app.route("/")
def hello_world():
    return "Welcome to the CMS stream tool web server"


@app.route('/statscard/')
def projects():
    return "The stats page"


class Stat:
    def __init__(self, title, value, username, kit):
        self.title = title
        self.value = value
        self.username = username
        self.kit = kit


stats = [Stat("Most Kills", "65", "b0squet", "archer")]




@app.route('/statscard/content/', methods=["GET"])
def stats_content():
    return render_template("stats_card_content.html", stats_for_card=stats, map_info="Map 1 - Adrenaline I")


app.run(host="localhost", port=5000, debug=False)