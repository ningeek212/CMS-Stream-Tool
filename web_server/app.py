from flask import Flask, render_template
from flask_classy import FlaskView, route

app = Flask(__name__)

app.template_folder = "render_templates"
app.static_folder = "static"


from web_server.server.ConfigView import ConfigView



ConfigView.register(app)


@app.route("/")
def home():
    return render_template("home/home.html")


if __name__ == '__main__':
    app.run()