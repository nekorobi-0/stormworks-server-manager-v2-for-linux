import json
import xmltodict
import xml.etree.ElementTree as ET
class profile():
    def __init__(self,profile_id:int) -> None:
        if profile_id == -1:#新規生成
            with open("data/profiles_data.json","r")as f:
                data = json.load(f)
            data["count"] +=1
            profile_id = str(data["count"])
            j = json.dump(data)
            with open("data/profiles/profiles_data.json","w")as f:
                f.write(j)
        else:
            self.profile_id = profile_id
            tree = ET.parse(f"data/profiles/{profile_id}.xml")
            xml_data = tree.getroot()
            xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')
            self.setting = dict(xmltodict.parse(xmlstr))
            with open("data/profiles_data.json","r")as f:
                data = json.load(f)
            self.permission = data
            self.profile_id = profile_id
        
    def apply(self):
        string = xmltodict.unparse(self.setting, pretty=True)
        with open(f"data/profiles/{self.profile_id}.xml","w")as f:
            f.write(string)