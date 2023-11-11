import json
from misskey import Misskey
import settings
import random
import string
class user:
    def __init__(self,FileOrToken,mode) -> None:
        if mode == "json":
            file = FileOrToken
            with open(file) as f:
                data = json.load(f)
            self.token = data["token"]
            self.profiles = data["profiles"]
            self.get_data()
            self.profilelimit = data["profilelimit"]
            self.seacret = data["seacret"]
            self.serverlim = data["serverlim"]
        elif mode == "new":
            misskey_token = FileOrToken
            self.token = misskey_token
            self.get_data()
            self.profiles = []
            self.profilelimit = settings.profilelimit
            self.seacret = randomname(100)
            self.export_file()
            print("ok")
            self.serverlim = 1
        self.runningservers = []
    def get_data(self):
        mk = Misskey("stormskey.works",i=self.token)
        self.mk = mk.i()
        self.id = self.mk["id"]
        self.name = self.mk["username"]
        self.avatarurl = self.mk["avatarUrl"]
    def add_profile(self,profile):
        if len(self.profiles) > self.profilelimit:
            self.profiles.append(profile)
        else:
            raise Exception(f"too many plofiles has user:({self.name})")
    def export_file(self):
        data = {
            "seacret":self.seacret,
            "profilelimit":self.profilelimit,
            "token":self.token,
            "profiles":self.profiles,
            "serverlim":self.serverlim
        }
        with open(f"data/users/{self.id}.json", mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    def cookiedata(self):
        data = {
            "username":self.name,
            "id":self.id,
            "seacret":self.seacret,
            "avatarurl":self.avatarurl,
            "profilelimit":self.profilelimit,
            "serverlim":self.serverlim
        }
        return json.dumps(data,ensure_ascii=False, indent=4)
def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)