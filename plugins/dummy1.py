import time
from bt.plugin import BastPlugin

class dummy1(BastPlugin):
  def run(self, **conf):
    #log.info("dummy plugin is for demonestration purposes")
    print conf