from misskey import Misskey
import json
import websockets
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import glob
import os

maintainancing = False
pages_txt= {}
#load all pages
files = [os.path.basename(p) for p in glob.glob('websv/**', recursive=True)
       if os.path.isfile(p)]
for page in files:
    with open(f"websv/{page}",mode="r",encoding="utf-8") as f:
        txt = f.read()
    pages_txt[page] = txt
    print(f"{page},",end="")
print("\nended importing")


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

    def do_GET(self):
        def redirect(terg="index.html"):
            self.send_response(302)
            self.send_header('Location', terg)
            self.end_headers()
        req = self.requestline[5:].split()[0]
        if req in pages_txt:
            svt = pages_txt[req]
        else:
            svt = pages_txt["404.html"]
        self.wfile.write(svt.encode())
    
    def do_POST(self):
        
        self._set_headers()
        self.wfile.write("msg".encode())

def run_http_server(server_class=HTTPServer, handler_class=S, port=8888):

	# startup HTTP server
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('HTTP server started....')
	httpd.serve_forever()

print(mk.users_show("9grxrmn5np")['avatarUrl'])
mk.notes_create(text="@null これはテストです",visibility="specified",visible_user_ids=["9grxrmn5np"])
asyncio.run(getTL(token))
