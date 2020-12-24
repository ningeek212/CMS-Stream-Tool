import keyboard
from utils.utils import get_config_dict
from time import sleep


def setup_hotkeys():
    config_dict = get_config_dict()
    for key in config_dict.keys():
        if key.split("_")[0] == "hotkey":
            keyboard.add_hotkey(config_dict[key]["value"], eval(key))


class HotkeyCodesDetector:
    def __init__(self):
        self.finished = False
        self.combination = None
        self.keys_pressed = []
        self.key_names = []
        self.hook = None

    def find_hotkey_combination(self, timeout):
        self.hook = keyboard.hook(self.process_event, suppress=False)
        count = 0
        while not self.finished:
            sleep(0.1)
            count += 1
            if count >= timeout*10:
                return False
        string_list = [str(element) for element in self.key_names]
        return self.combination, "+".join(string_list)

    def process_event(self, event):
        if event.scan_code not in self.keys_pressed:
            self.keys_pressed.append(event.scan_code)
            self.key_names.append(event.name)
        if event.event_type == "up":
            keyboard.unhook(self.hook)
            self.combination = tuple(self.keys_pressed)
            self.finished = True


def hotkey_scene_highlights():
    print("Switching to Scene: Highlights")


def hotkey_scene_minecraft():
    print("Switching to Scene: Minecraft")


def hotkey_scene_next_map():
    print("Switching to Scene: Next Map")