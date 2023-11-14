import settings,os,shutil
servers = []
for i in range(settings.server_count):
    servers.append(False)
    if not(os.path.isdir(f"stw/sv{i}")):
        os.mkdir(f"stw/sv{i}")
        shutil.copy("stw/server64.exe",f"stw/sv{i}.exe")
def Allocator()->int:
    global servers
    for i,sv in enumerate(servers):
        if not(sv):
            servers[i] = True
            return i
    else:
        raise Exception("There are no unused server")