import time
from bt.plugin import BastPlugin

class dummy2(BastPlugin):
    def run(self, **conf):
        while True:
            #log.info("dummy plugin is for demonestration purposes")
            print conf
            time.sleep(2)
