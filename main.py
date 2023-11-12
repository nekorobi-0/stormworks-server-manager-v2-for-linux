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
servers = {}
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
            try:
                with open(f"websv/{page}",mode="r",encoding="utf-8") as f:
                    txt = f.read()
                pages_txt[page] = txt
            except IsADirectoryError:
                pass
    except PermissionError:
        pass
print("ended webserver importing")
#/load all pages
#load all profiles
files = [os.path.basename(p) for p in glob.glob('data/profiles/**', recursive=True)
       if os.path.isfile(p)]
for file in files:
    try:
        id = int(file[:-4])
        profiles[id] = profile.profile(id)
    except ValueError:
        pass
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
            elif (req[5:] == "createprof"):
                content_len = int(self.headers.get('Content-Length'))
                output = str(self.rfile.read(content_len).decode('utf-8'))
                data = json.loads(output)
                user = users[data["id"]]
                if (user.seacret == data["seacret"]
                    and len(user.profiles) < user.profilelimit):
                    newprof = profile.profile(-1)
                    profiles[newprof.profile_id] = newprof
                    user.profiles.append({"name":"newprofile","id":newprof.profile_id})
                user.export_file()
                self._set_headers()
                self.wfile.write("success".encode())
            elif req[5:] == "login_with_misskey":
                session.misskeylogin(self,users,mk,sessions)
            elif req[5:10] == "auth/":
                try:
                    id = int(req[10:])
                    if id in sessions:#いい感じ
                        sessions[id].auth(self)
                        sessions.pop(id)
                    else:
                        self._set_headers()
                        self.wfile.write("failed".encode())
                except ValueError:
                    pass
            elif req[5:] == "get_profiles":#プロファイル一覧の取得
                content_len = int(self.headers.get('Content-Length'))
                output = str(self.rfile.read(content_len).decode('utf-8'))
                data = json.loads(output)
                print(data)
                user = users[data["id"]]
                if user.seacret == data["seacret"]:#照合
                    profs = user.profiles
                    data_s = {}
                    for pro in profs:
                        data_s[pro["id"]] = pro["name"]
                        print(data_s)
                    txt = json.dumps(data_s,ensure_ascii=False, indent=4)
                    self._set_headers()
                    self.wfile.write(txt.encode())
                else:
                    self._set_headers()
                    self.wfile.write("failed".encode())
            elif req[5:] == "get_profile":
                print("ok")
                content_len = int(self.headers.get('Content-Length'))
                output = str(self.rfile.read(content_len).decode('utf-8'))
                data = json.loads(output)
                user = users[data["id"]]
                if (user.seacret == data["seacret"] and
                    int(data["proid"]) in ([int(d.get('id')) for d in user.profiles])):#照合:
                    data_s = {}
                    for set in settings.available_settings:
                        data_s[set] = profiles[int(data["proid"])].setting["server_data"][f"@{set}"]
                    txt = json.dumps(data_s,ensure_ascii=False, indent=4)
                    self._set_headers()
                    self.wfile.write(txt.encode())
            elif req[5:] == "get_admin":
                content_len = int(self.headers.get('Content-Length'))
                output = str(self.rfile.read(content_len).decode('utf-8'))
                data = json.loads(output)
                user = users[data["id"]]
                if (user.seacret == data["seacret"] and
                    int(data["proid"]) in ([int(d.get('id')) for d in user.profiles])):#照合:
                    pro = profiles[int(data["proid"])]
                    data_s = {}
                    if pro.setting["server_data"]["admins"] != None:
                        for set in pro.setting["server_data"]["admins"]["id"]:
                            admins = pro.setting["server_data"]["admins"]["id"]
                            print(set)
                            if int(set["@value"]) >0: 
                                data_s[int(set["@value"])] = "rocamisaki"
                    else:
                        data_s[-1] = "rocamisaki"
                    txt = json.dumps(data_s,ensure_ascii=False, indent=4)
                    self._set_headers()
                    self.wfile.write(txt.encode())
            elif req[5:] == "runningserver":
                content_len = int(self.headers.get('Content-Length'))
                output = str(self.rfile.read(content_len).decode('utf-8'))
                data = json.loads(output)
                user = users[data["id"]]
                if user.seacret == data["seacret"]:#照合
                    svs = user.runningservers
                    data_s = {}
                    for sv in svs:
                        data_s[sv] = "rocami"
                    txt = json.dumps(data_s,ensure_ascii=False, indent=4)
                    self._set_headers()
                    self.wfile.write(txt.encode())
                else:
                    self._set_headers()
                    self.wfile.write("failed".encode())
            elif req[5:] == "oparation":#プロファイルの起動,編集,削除
                content_len = int(self.headers.get('Content-Length'))
                output = str(self.rfile.read(content_len).decode('utf-8'))
                data = json.loads(output)
                print(data)
                user = users[data["id"]]
                print(user.profiles)
                if (user.seacret == data["seacret"] and
                    data["proid"] in user.runningservers):
                    print("sv")
                    sv = servers[data["proid"]]
                    if data["mode"] == "stop":
                        sv.stop()
                        user.runningservers.remove(data["proid"])
                        servers.pop(data["proid"])
                        del sv
                    self._set_headers()
                    self.wfile.write("success".encode())
                elif (user.seacret == data["seacret"] and
                    int(data["proid"]) in [d.get('id') for d in user.profiles]):
                    print(data["mode"])
                    pro = profiles[int(data["proid"])]
                    if data["mode"] == "run":
                        if (len(servers) < settings.server_count and 
                            len(user.runningservers) < user.serverlim):
                            s = server.server(pro,user)
                            servers[data["proid"]] = s
                            user.runningservers.append(data["proid"])
                    elif data["mode"] == "delete":
                        for ind,pror in enumerate(user.profiles):
                            if pror["id"] == int(data["proid"]):
                                user.profiles.pop(ind)
                        user.export_file()
                        pro.delete()
                    elif data["mode"] == "addadmin":
                        admins = pro.setting["server_data"]["admins"]["id"]
                        if admins == None:
                            n = {"id":[{"@value":data["add_id"]}]}
                        else:
                            n = {"id":(admins + [{"@value":data["add_id"]}])}
                        pro.setting["server_data"]["admins"] = n
                        pro.apply()
                    elif data["mode"] == "save":
                        print(pro.setting)
                        for i in data["datas"]:
                            if i in settings.available_settings:
                                pro.setting["server_data"][f"@{i}"] = data["datas"][i]
                        print(pro.setting)
                        pro.apply()
                        pass
                    elif data["mode"] == "deladmin":
                        admins = pro.setting["server_data"]["admins"]["id"]
                        print(admins)
                        for admin in enumerate(admins):
                            if admin[1]["@value"] == str(data["id2del"]):
                                admins.pop(admin[0])
                        n = {"id":admins}
                        pro.setting["server_data"]["admins"] = n
                        pro.apply()
                    self._set_headers()
                    self.wfile.write("success".encode())
                else:
                    self._set_headers()
                    self.wfile.write("failed".encode())
                    


def run_http_server(server_class=HTTPServer, handler_class=S, port=8888):

	# startup HTTP server
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('HTTP server started....')
	httpd.serve_forever()

"""t = threading.Thread(target=run_http_server)
t.start()
asyncio.run(getTL(token))"""
run_http_server()
print("fin")