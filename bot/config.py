import json

with open("config.json") as config_file:
    data = json.load(config_file)

TG_TOKEN = data["tg_token"]
