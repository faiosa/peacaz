import json
import os

SETTINGS_FILE = os.path.join("config", "settings.json")
SEPAR_SETTINGS_FILE = os.path.join("config", "separ_settings.json")

def load_settings():
    return load_settings_from_file(SETTINGS_FILE)


def load_settings_from_file(settings_file):
    try:
        with open(os.path.abspath(settings_file), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "global_settings": {"theme": "Світла", "language": "Українська"},
            "controller_values": {"1": {"name": "Default"}},
            "switchboard_settings": {"serial_port": "port"},
        }
    except json.JSONDecodeError:
        return {}


def save_settings(settings):
    with open(os.path.abspath(SETTINGS_FILE), "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)
