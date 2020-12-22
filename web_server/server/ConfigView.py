from flask_classy import FlaskView, route
from flask import render_template, jsonify, request
from json import load, dump, loads

CONFIG_PATH = "misc/config.json"

with open(CONFIG_PATH) as json_file:
    config_dict = load(json_file)

ordered_keys = sorted(config_dict, key=lambda x: config_dict[x]["setting_id"])
# Order the list of settings by the "setting_id" value to prevent their order getting scrambled


class ConfigView(FlaskView):
    def index(self):
        return render_template("config/config.html", settings=config_dict, keys=ordered_keys)

    @route("/dict")
    def dict(self):
        return jsonify(config_dict)

    @route("/submit", methods=["POST"])
    def submit(self):
        global config_dict
        for setting in request.json.keys():
            # Try converting json data back to an int or a float where necessary
            if "." in request.json[setting]["value"]:
                try:
                    request.json[setting]["value"] = float(request.json[setting]["value"])
                except ValueError:
                    pass
            else:
                try:
                    request.json[setting]["value"] = int(request.json[setting]["value"])
                except ValueError:
                    pass
        with open(CONFIG_PATH, 'w') as outfile:
            config_dict = request.json
            dump(request.json, outfile, indent=2)
            print("Config updated successfully")
            return jsonify({"success_message": "Config file updated"})
