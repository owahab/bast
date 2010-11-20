import sys
import shutil
from bt.plugin import BastPlugin

class files(BastPlugin):
  
  def run(self, directory):
    dir_name = self.backup_id + '--files'
    self.log.debug("Backing up directory %s." % directory)
    try:
      shutil.copytree(directory, dir_name, symlinks=True)
    except:
      self.log.error('File backup cancelled! (%s)' % sys.exc_info()[1])
    else:
      self.compress(dir_name)
      self.log.debug('Files backup complete.')
      self.status = True