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
maintainancing = False
pages_txt= {}
#load all users
users = []
files = [os.path.basename(p) for p in glob.glob('data/users/**', recursive=True)
       if os.path.isfile(p)]
for file in files:
    users.append(user(f"data/uers/{file}","json"))
print("ended user importing")
#/load alll users
#load all pages
files = [os.path.basename(p) for p in glob.glob('websv/**', recursive=True)
       if os.path.isfile(p)]
for page in files:
    with open(f"websv/{page}",mode="r",encoding="utf-8") as f:
        txt = f.read()
    pages_txt[page] = txt
print("ended webserver importing")
#/load all pages

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
        if req =="logon.html":
            svt = pages_txt[""]
        elif req in pages_txt:
            svt = pages_txt[req]
        else:
            svt = pages_txt["404.html"]
        self.wfile.write(svt.encode())
    def do_POST(self):
        req = self.requestline[5:].split()[0]
        if req[:3] == "api":
            if req[3:]=="logon_url":
                t = threading.Thread(target=session.miauth,args=(self,users))
                t.start()
            elif req[3:] == "login_with_misskey":
                t = threading.Thread(target=session.misskeylogin,args=(self,users,mk))
            elif req[3:7] == "auth":
                id = req[7:]


def run_http_server(server_class=HTTPServer, handler_class=S, port=8888):

	# startup HTTP server
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('HTTP server started....')
	httpd.serve_forever()

print(mk.users_show("9grxrmn5np")['avatarUrl'])
mk.notes_create(text="@null これはテストです",visibility="specified",visible_user_ids=["9grxrmn5np"])
t = threading.Thread(target=run_http_server)
t.start()
asyncio.run(getTL(token))
