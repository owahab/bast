import subprocess
from bt.plugin import BastPlugin

class mysql(BastPlugin):
  mysqldump = 'mysqldump'

  def run(self, username, password, host, dbname):
    p = ''
    if password:
      p = '-p' + password
    
    filename = self.backup_id + '-mysql-' + dbname + '.sql'
    subprocess.call([
      self.mysqldump,
      '-u' + username,
      p,
      '-h' + host,
      '-r' + filename,
      dbname
    ])
    self.compress(filename)
