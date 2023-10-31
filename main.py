from misskey import Misskey
import json
import websockets
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import glob
import os
import class_session as session
import class_profile as profile
import class_server as server
import class_user as user
import threading
import settings
maintainancing = False
pages_txt= {}
#load all users
users = {}
sessions = {}
profiles = {}
files = [os.path.basename(p) for p in glob.glob('data/users/**', recursive=True)
       if os.path.isfile(p)]
for file in files:
    users[file[:-5]] = user.user(f"data/users/{file}","json")
print("ended user importing")
#/load alll users
#load all pages
files = glob.glob('websv/**', recursive=True)
for page in files:
    page = page.replace("\\","/")
    page = page.replace('websv/',"")
    try:
        if page != "":
            with open(f"websv/{page}",mode="r",encoding="utf-8") as f:
                txt = f.read()
            pages_txt[page] = txt
    except PermissionError:
        pass
print("ended webserver importing")
#/load all pages
#load all profiles
users = {}
sessions = {}
files = [os.path.basename(p) for p in glob.glob('data/profiles/**', recursive=True)
       if os.path.isfile(p)]
for file in files:
    id = file[:-4]
    profiles[id] = profile.profile(id)
print("ended profile importing")
#/load all profiles

with open("config.json","r")as f:
    data = json.load(f)
token = data["token"]
mk = Misskey("stormskey.works",i=token)
async def getTL(token):
    global output
    #TL取得
    while True:
        print("try to connect")
        uri = f"wss://stormskey.works//streaming?i={token}"
        async with websockets.connect(uri) as ws:
            await ws.send(json.dumps({
	            "type": 'connect',
	            "body": {
		            "channel": "localTimeline",
		            "id": "localTimeline",
                }
            }))
            print("connected")
            while True:
                try:
                    data = json.loads(await ws.recv())
                except websockets.exceptions.ConnectionClosedError:
                    break
                name = data["body"]["body"]["user"]["name"]
                text = data["body"]["body"]["text"]


class S(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def redirect(self,terg="index.html"):
        self.send_response(302)
        self.send_header('Location', terg)
        self.end_headers()
    def do_GET(self):
        req = self.requestline[5:].split()[0]
        if req[:9] == "api/auth/":
            svt = pages_txt["api/auth/success.html"]
        elif req =="logon.html":
            svt = pages_txt[""]
        elif req in pages_txt:
            svt = pages_txt[req]
        else:
            svt = pages_txt["404.html"]
        self._set_headers()
        self.wfile.write(svt.encode())
    def do_POST(self):
        global id
        req = self.requestline[5:].split()[0]
        if req[1:4] == "api":
            print(req[5:])
            if req[5:]=="logon_url":
                session.miauth(self,users)
                print(users)
            elif req[5:] == "login_with_misskey":
                session.misskeylogin(self,users,mk,sessions)
            elif req[5:10] == "auth/":
                try:
                    id = int(req[10:])
                    print(id)
                    if id in sessions:#いい感じ
                        print("login ok")
                        sessions[id].auth(self)
                    else:
                        self._set_headers()
                        self.wfile.write("failed".encode())
                except ValueError:
                    pass
            elif req[5:] == "get_profiles":
                content_len = int(self.headers.get('Content-Length'))
                output = str(self.rfile.read(content_len).decode('utf-8'))
                data = json.loads(output)
                user = users[data["id"]]
                profs = user.profiles
                data = {}
                for pro in profs:
                    data[profiles[pro["id"]]] = data[profiles[pro["name"]]]
                txt = json.dumps(data,ensure_ascii=False, indent=4)
                self._set_headers()
                self.wfile.write(txt.encode())


def run_http_server(server_class=HTTPServer, handler_class=S, port=8888):

	# startup HTTP server
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('HTTP server started....')
	httpd.serve_forever()

t = threading.Thread(target=run_http_server)
t.start()
asyncio.run(getTL(token))
print("fin")