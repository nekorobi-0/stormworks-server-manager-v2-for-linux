import json
import settings
class user:
    def __init__(self,file) -> None:
        with open(file) as f:
            data = json.load(f)
    def __init__(self,misskey_token):
        self.profiles = []
        self.profilelimit = settings.profilelimit
    def add_profile(self,profile):
        if len(self.profiles) > self.profilelimit:
            self.profiles.append(profile)
        else:
            raise Exception(f"too many plofiles has user:({self.name})")
    def export_file(self):
        pass