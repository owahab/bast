import time
class dummy1():
    def backup(self, conf, *args):
        while True:
            #log.info("dummy plugin is for demonestration purposes")
            print conf
            time.sleep(2)
