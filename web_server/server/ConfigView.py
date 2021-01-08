from flask_classy import FlaskView, route
from flask import render_template, jsonify, request
from json import load, dump, loads
from utils.hotkeys import HotkeyCodesDetector

CONFIG_PATH = "misc/config.json"


def get_config_dict():
    with open(CONFIG_PATH) as json_file:
        return load(json_file)


def write_config(dict_to_write):
    with open(CONFIG_PATH, 'w') as outfile:
        dump(dict_to_write, outfile, indent=2)

class ConfigView(FlaskView):
    def index(self):
        config_dict = get_config_dict()

        ordered_keys = sorted(config_dict, key=lambda x: config_dict[x]["setting_id"])
        return render_template("config/config.html", settings=config_dict, keys=ordered_keys)

    @route("/dict")
    def dict(self):
        return jsonify(get_config_dict())

    @route("/maptest")
    def map_test(self):
        return render_template("config/maptest.html")

    @route("/submit", methods=["POST"])
    def submit(self):
        config_dict = get_config_dict()
        for setting in request.json.keys():
            if request.json[setting]["type"] == "input" or request.json[setting]["type"] == "select":
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

    @route("/change_hotkey", methods=["GET"])
    def get_hotkey(self):
        result = HotkeyCodesDetector().find_hotkey_combination(10)
        if result is False:
            return jsonify({
                "success": "false",
                "error": "You took too long to press a hotkey combination"
            })
        else:
            hotkey_name = request.args.get("hotkey_name")
            config = get_config_dict()
            config[hotkey_name]["value"] = result[0]
            config[hotkey_name]["hotkey_string"] = result[1]
            write_config(config)
            return jsonify({
                "success": "true",
                "scan_codes": result[0],
                "hotkey_string": result[1]
            })

