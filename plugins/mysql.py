import subprocess
from bt.plugin import BastPlugin

class mysql(BastPlugin):
    mysqldump = 'mysqldump'

    def run(self, username, password, host, dbname):
        subprocess.call([self.mysqldump,
                         '-u' + username,
                         '-p' + password,
                         '-h' + host,
                         '-r' + self.backup_id + '-mysql-' + dbname + '.sql',
                         dbname])
