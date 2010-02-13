import time

class dummy2():
    def run(self, **conf):
        while True:
            #log.info("dummy plugin is for demonestration purposes")
            print conf
            time.sleep(2)
