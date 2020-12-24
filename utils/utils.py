from json import load, dump, loads

CONFIG_PATH = "misc/config.json"

def get_config_dict():
    with open(CONFIG_PATH) as json_file:
        config_dict = load(json_file)
        return config_dict