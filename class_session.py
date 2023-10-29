import random
import time
import settings
from misskey import MiAuth,Misskey
import misskey
import asyncio
import time
import class_user as user
import settings
import threading
class session:
    def __init__(self,user) -> None:
        self.id = random.randint(0,2**63)
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
    self._set_headers()
    self.wfile.write(mia.url.encode())
    t = threading.Thread(target=miauthcheck,args=(users,mia))
    t.start()
def miauthcheck(users,mia):
    for i in range(60):
        try:
            users.append(user.user(mia.mia.check(),"new"))
            break
        except misskey.exceptions.MisskeyMiAuthFailedException:
            pass
        time.sleep(0.5)
def misskeylogin(self,users,mk,id):
    content_len = int(self.headers.get('Content-Length'))
    output = str(self.rfile.read(content_len).decode('utf-8'))
    username = output.replace("https://stormskey.works/@","")
    for user in users:
        if user.name == username:
            break
    else:
        self._set_headers()
        self.wfile.write("".encode())
        return
    session_now = session(user)
    url = f"http://{settings.server_addres}/api/auth/{session_now.id}"
    mk.notes_create(text=f"""@{user.name}
        ログインがありました
        心当たりがなければ無視してください
        認証url:
        {url}"""
        ,visibility="specified",visible_user_ids=[user.id,]
    )
    r = settings.sessiontime*10
    for i in range(r):
        if session_now.id in id:
            data = user.cookiedata()
            self._set_headers()
            self.wfile.write(data.encode())
        time.sleep(0.1)