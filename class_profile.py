import json
import xmltodict
import xml.etree.ElementTree as ET
import os
class profile():
    def __init__(self,profile_id:int) -> None:
        if profile_id == -1:#新規生成
            with open("data/profiles_data.json","r")as f:
                data = json.load(f)
            print(data)
            data["count"] += 1
            print(data)
            self.profile_id = data["count"]
            j = json.dumps(data)
            with open("data/profiles_data.json","w")as f:
                f.write(j)
            tree = ET.parse(f"data/profiles/0.xml")
            xml_data = tree.getroot()
            xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')
            self.setting = dict(xmltodict.parse(xmlstr))
            self.apply()
        else:
            self.profile_id = profile_id
            tree = ET.parse(f"data/profiles/{profile_id}.xml")
            xml_data = tree.getroot()
            xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')
            self.setting = dict(xmltodict.parse(xmlstr))
            self.profile_id = profile_id
        self.path = f"data/profiles/{self.profile_id}.xml"

        
    def apply(self):
        string = xmltodict.unparse(self.setting, pretty=True)
        with open(f"data/profiles/{self.profile_id}.xml","w")as f:
            f.write(string)
    def delete(self):
        os.remove(f"data/profiles/{self.profile_id}.xml")
        del self