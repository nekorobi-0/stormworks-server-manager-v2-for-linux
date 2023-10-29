import subprocess
import ServerAllocator
class server:
    def __init__(self,profile,user) -> None:
        self.RunningProfile = False
        self.timelimit = None
        self.dir = ServerAllocator.Allocator()
        self.HavePermissionUser = None
        self.HavePermissionUser.append(user)
        with open(profile.path,"r") as f:
            prof = f.read
        prof.replase('port="port"',f'port="{25570+self.dir*2}"')
        with open(f"{self.dir}/settings.xml","w")as f:
            f.write(prof)
        self.RunningProfile = profile
        self.server = subprocess.Popen(f"exec wine server64.exe +server_dir ~/server/stw/{self.dir}")
    def stop(self):
        if self.server != None:
            self.server.kill()
    def check_status(self):
        if self.server != None:
            if self.server.call() != None:
                return True
        del self
        return False
    def __del__(self):
        with open(f"{self.dir}/settings.xml","w")as f:
            f.write("")