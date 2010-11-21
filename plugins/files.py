import os
import sys
import shutil
from bt.plugin import BastPlugin

class files(BastPlugin):
  
  def run(self, directory, symlinks='copy'):
    dir_name = self.backup_id + '--files'
    self.log.debug("Backing up directory %s." % directory)
    if symlinks == 'follow':
      symlinks_mode = 2
    elif symlinks == 'copy':
      symlinks_mode = 1
    else:
      symlinks_mode = 0
    try:
      self.copytree(directory, dir_name, symlinks=symlinks_mode)
    except:
      self.log.error('File backup cancelled! (%s)' % sys.exc_info()[1])
    else:
      self.compress(dir_name)
      self.log.debug('Files backup complete.')
      self.status = True
    
  def copytree(self, src, dst, symlinks=0, ignore=None):
    '''
    A modified version of os.copytree to add more options like:
    symlinks: ignore them totally
    '''
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()
    os.makedirs(dst)
    errors = []
    for name in names:
      if name in ignored_names:
          continue
      srcname = os.path.join(src, name)
      dstname = os.path.join(dst, name)
      try:
          if os.path.islink(srcname):
            if symlinks == 1:
              linkto = os.readlink(srcname)
              os.symlink(linkto, dstname)
            elif symlinks == 2:
              shutil.copy2(srcname, dstname)
          elif os.path.isdir(srcname):
              shutil.copytree(srcname, dstname, symlinks, ignore)
          else:
              shutil.copy2(srcname, dstname)
      except (IOError, os.error), why:
          errors.append((srcname, dstname, str(why)))
      # catch the Error from the recursive copytree so that we can
      # continue with other files
      except ValueError, err:
          errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise ValueError(errors)