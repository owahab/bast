import time
from bt.plugin import BastPlugin

class dummy2(BastPlugin):
  def run(self, **conf):
    print conf
