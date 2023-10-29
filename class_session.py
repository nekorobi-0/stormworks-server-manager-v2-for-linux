import random
import time
import settings
from misskey import MiAuth
import asyncio
import time
class session:
    def __init__(self,user) -> None:
        self.id = random.randint(0,2^256)
        self.user = user
        self.time = time.time()
    def living(self):
        if (time.time() - self.time) > settings.sessiontime:
            return True
        else:
            del self
            return False
class miatuth_session:
    def __init__(self) -> None:
        self.mia = MiAuth(
            "stormskey.works",
            name="NullStormworksServerManager",
            permission=[
                "read:account"
            ]
        )
        self.url = self.mia.generate_url()
    def token(self) ->str:
        token = self.mia.check()
        return token
def miauth(self):
    mia = miatuth_session()
    self.redirect(mia.url)
    time.sleep(1)
    mia.token