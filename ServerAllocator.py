import settings
servers = []
for i in range(settings.server_count):
    servers.append(False)
def Allocator()->int:
    global servers
    for i,sv in enumerate(servers):
        if not(sv):
            servers[i] = True
            return i
    else:
        raise Exception("There are no unused server")