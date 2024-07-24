import json

class AppConfig:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = {
            "init": True,
            "inference":{
                "method": {
                    "server": "local",
                    "key": None,
                    "url": None
                },
                "option": {
                    "object_detection": True,
                    "scene_classification": True,
                    "ocr": True,
                    "caption_generation": False
                }
            },
            "folders": []
        }
        self.defConfig = self.config

    def write_config(self, content):
        with open(self.config_file, 'w') as file:
            json.dump(content, file, indent=4)

    def read_config(self):
        with open(self.config_file, 'r') as file:
            self.config = json.load(file)
        return self.config