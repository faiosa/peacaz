import json
from config.settings import SETTINGS_FILE


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
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
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)
