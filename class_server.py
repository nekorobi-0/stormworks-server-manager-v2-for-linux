import subprocess
import ServerAllocator
class server:
    def __init__(self,profile,user) -> None:
        self.RunningProfile = False
        self.timelimit = None
        self.dir = ServerAllocator.Allocator()
        self.HavePermissionUser = []
        self.HavePermissionUser.append(user)
        with open(profile.path,"r") as f:
            prof = f.read()
        prof = prof.replace('portrep',f'{25570+self.dir*2}')
        with open(f"stw/sv{self.dir}/server_config.xml","w")as f:
            f.write(prof)
        self.RunningProfile = profile
        self.server = subprocess.Popen(f"exec wine stw/server64.exe +server_dir ~/server/stw/sv{str(self.dir)}",
            creationflags=subprocess.REALTIME_PRIORITY_CLASS)
        #self.server = subprocess.Popen(f"sv_fake.bat",shell=True)
        print("success")
    def stop(self):
        if self.server != None:
            self.server.kill()
            ServerAllocator.servers[self.dir] = False
    def check_status(self):
        if self.server != None:
            if self.server.call() != None:
                return True
        del self
        return False
    def __del__(self):
        with open(f"stw/sv{self.dir}/settings.xml","w")as f:
            f.write("")