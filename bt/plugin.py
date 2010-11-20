import sys
import os
import shutil
import tarfile

class BastPlugin:
  def __init__(self, log, backup_id):
    self.backup_id = backup_id
    self.log = log
    self.status = False
  
  def compress(self, file_or_dir):
    self.log.debug("Compressing directory %s." % file_or_dir)
    name = file_or_dir + '.tar.gz'
    f = tarfile.open(name, 'w:gz')
    f.add(file_or_dir, recursive=True)
    f.close()
    if os.path.isdir(file_or_dir) == True:
      self.log.debug("Deleting directory %s." % file_or_dir)
      shutil.rmtree(file_or_dir)
    else:
      self.log.debug("Deleting file %s." % file_or_dir)
      os.remove(file_or_dir)