import random
import time
import settings
from misskey import MiAuth,Misskey
import asyncio
import time
import class_user as user
import settings
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
def miauth(self,users):
    mia = miatuth_session()
    self.wfile.write(mia.url.encode())
    time.sleep(3)
    users.append(user.user(mia.token))
def misskeylogin(self,users,mk):
    print(self.rfile)
    username = self.rfile.replase("https://stormskey.works/@","")
    for user in users:
        if user.name == username:
            user_login = user
            break
    else:
        return
    session_now = session(user_login)
    url = f"http://{settings.server_addres}/{session_now.id}"
    mk.notes_create(text=f"@{user_login.username}",visibility="specified",visible_user_ids=["9grxrmn5np"])
    while True:
        time.sleep(0.1)
        break