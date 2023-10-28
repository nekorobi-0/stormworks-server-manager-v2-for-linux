import random
import time
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