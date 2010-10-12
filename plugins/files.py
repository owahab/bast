import shutil
from bt.plugin import BastPlugin

class files(BastPlugin):
  
  def run(self, directory):
    dir_name = self.backup_id + '-files'
    shutil.copytree(directory, dir_name)
    self.compress(dir_name)