import sys
import subprocess
from bt.plugin import BastPlugin

class mysql(BastPlugin):
  mysqldump = 'mysqldump'

  def run(self, host, username, dbname, password = ''):
    p = ''
    if password:
      p = '-p' + password
    
    filename = self.backup_id + '--mysql-' + dbname + '.sql'
    self.log.debug("Backing up database %s." % dbname)
    try:
      subprocess.check_call([
        self.mysqldump,
        '-h' + host,
        '-u' + username,
        '-r' + filename,
        dbname,
        p
      ], stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    except:
      self.log.error('MySQL backup cancelled! (Error executing mysqldump)')
    else:
      self.compress(filename)
      self.log.debug('MySQL backup complete.')
      self.status = True