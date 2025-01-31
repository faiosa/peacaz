import json
import os

from PyQt5.QtCore import QStandardPaths


class Tweak():
    def __init__(self):
        self.domain = "peacaz"
        self.name = "tweak"
        self.paths = [
            os.path.join(os.path.dirname(str(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation))), self.domain, self.name + ".json"),
            os.path.join(os.path.dirname(__file__), self.name + ".json")
        ]



    def get_settings(self):
        for p in self.paths:
            print(f"CHECKING path = {os.path.abspath(p)}")
            if os.path.isfile(p):
                try:
                    with open(os.path.abspath(p), "r", encoding="utf-8") as f:
                        return json.load(f)
                except FileNotFoundError:
                    continue
        raise FileNotFoundError

    def write_settings(self, settings):
        path = self.paths[0]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print(f"WRITING to path = {path}")
        with open(self.paths[0], "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4, ensure_ascii=False)
            file.close()

    def del_settings(self):
        path = self.paths[0]
        if os.path.isfile(path):
            try:
                os.remove(path)
            except Exception:
                return False
            return True
        return False