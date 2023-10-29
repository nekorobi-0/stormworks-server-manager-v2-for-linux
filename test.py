import json
from misskey import Misskey
with open("config.json","r")as f:
    data = json.load(f)
token = data["token"]
mk = Misskey("stormskey.works",i=token)
print(mk.i())