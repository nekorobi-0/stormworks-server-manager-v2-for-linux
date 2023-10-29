import json
from misskey import Misskey
import settings
class user:
    def __init__(self,file,extension) -> None:
        with open(file) as f:
            data = json.load(f)
        mk = Misskey("stormskey.works",i=)
        data["token"]
        self.profiles = data["profiles"]
        self.get_data()
        self.profilelimit = data["profileslimit"]
    def __init__(self,misskey_token):
        self.token = misskey_token 
        self.profiles = []
        self.avatarurl = self.mk.avatarUrl
        self.profilelimit = settings.profilelimit
        self.get_data()
    def get_data(self):
        mk = Misskey("stormskey.works",i=self.token)
        self.mk = mk.i()
        self.id = self.mk.id
        self.name = self.mk.name
    def add_profile(self,profile):
        if len(self.profiles) > self.profilelimit:
            self.profiles.append(profile)
        else:
            raise Exception(f"too many plofiles has user:({self.name})")
    def export_file(self):
        pass