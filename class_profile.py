import json
import xmltodict
class profile():
    def __init__(self) -> None:
        with open("data/profiles/profiles_data.json","r")as f:
            data = json.load(f)
        data["count"] +=1
        profile_id = str(data["count"])
        j = json.dump(data)
        with open("data/profiles/profiles_data.json","w")as f:
            f.write(j)
        self.profile_id = profile_id
    def __init__(self,profile_id:int)->None:
        self.setting = xmltodict.parse(f"data/profiles/{profile_id}.xml")
        self.profile_id = profile_id
    def apply(self):
        string = xmltodict.unparse(self.setting, pretty=True)
        with open(f"data/profiles/{self.profile_id}.xml","w")as f:
            f.write(string)