
__version__ = '0.2.0'

import sys
import os
import datetime
import time
import shutil
import threading

class bast(object):
    def __init__(self):
        """
        Initializing
        """
        # Initialize command-line options
        self.__init_options()
        # Define project name
        self.project_name = os.path.splitext(os.path.basename(self.conf))[0]
        # Initialize config
        if not self.__init_config():
          # Exit
          return
        
        # Define project root directory
        self.project_dir = '%s/%s' %(self.config.get('BAST', 'root', '/var/backups'), self.project_name)
        # Now create it
        if not os.path.exists(self.project_dir):
          os.mkdir(self.project_dir)
        # Initialize logging
        self.__init_logging()
        # Initialize process name
        self.__init_proc_name()
        # Initialize path settings
        self.__init_path()  
        
        report = []
        if self.config.getboolean('BAST', 'backups', True):
          self.log.info("Starting backup for %s..." % self.project_name)
          # Backup IDs use this pattern: <project-name>--<yyyy.mm.dd>-<hh.mm.ss>
          now = datetime.datetime.now()
          # It is a requirement that project name doesn't contain any non-alphanumeric
          # characters, maybe we should validate that here.
          now_tag = '%04d.%02d.%02d-%02d.%02d.%02d' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
          backup_id = '%s--%s' % (self.project_name, now_tag)
          target = '%s/%s' % (self.project_dir, now_tag)
          self.log.debug('Creating directory %s.' % target)
          os.mkdir(target)
          self.log.debug('Changing directory to %s.' % target)
          os.chdir(target)
          
          plugins_status = {}
          threads = []
          # Dynamically load plugins based on configuration sections
          for section in self.config.sections():
            if section != 'BAST':
              try:
                m = self.__get_class("plugins.%s.%s" % (section, section))
                p = m(log=self.log, backup_id=backup_id)
                params = dict(self.config.items(section))
                params['status'] = plugins_status
                thread = threading.Thread(target=p.run, kwargs=params, name=section)
                thread.start()
                threads.append(thread)
              except KeyboardInterrupt:
                sys.exit()
    
          for t in threads:
            t.join()
          for k, v in plugins_status.items():
            s = 'Executed plugin %s: %s' % (k, ('OK' if v == True else 'Failed'))
            report.append(s)
            self.log.debug(s)
          self.log.debug('Changing directory to %s.' % self.project_dir)
          os.chdir(self.project_dir)
          # Compress
          self.log.debug('Compressing backup directory %s.' % now_tag)
          backup_file = self.compress(now_tag)
          # Gather few statistics
          s = 'Backup size is: %s' % self.human_size(os.path.getsize(backup_file))
          report.append(s)
          self.log.info(s)
          self.log.info('Backup complete!')
          backup_status = 'Successful: %s' % now_tag
          self.sync(backup_file)
        else:
          self.log.info('Backups for %s are suspended by configuration file. Exiting!' % self.project_name)
          backup_status = 'Suspended'
        # Rotate old backups
        report.append(self.rotate(self.config.getint('BAST', 'rotate', 10)))
        # Send notifications
        if self.config.getboolean('BAST', 'notifications', False):
          self.notify(backup_status, report)

    def __init_path(self):
        self.log.debug('Initializing path settings.')
        # Find out the location of bast's working directory, and insert it to sys.path
        basedir = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(os.path.join(basedir, "bast.py")):
            cwd = os.getcwd()
            if os.path.exists(os.path.join(cwd, "bast.py")):
                basedir = cwd
        sys.path.insert(0, basedir)

    def __init_options(self):
        from optparse import OptionParser
        parser = OptionParser(version="%prog 0.1b",
                                   description="BAST (Backup And Synchronization Tools)",
                                   usage="%prog [options] <conf-file>")
        parser.add_option('-v', '--verbose', action='store_true', dest='verbose', help='verbose output', default=False)
        parser.add_option('-d', '--debug', action='store_true', dest='debug', help='debug', default=False)

        (self.options, self.args) = parser.parse_args()
        if not len(self.args):
            parser.error('Expecting a configuration file to be given (try "--help" for help).')
        else:
            self.conf = self.args[0]
        
    def __init_logging(self):
      import logging
      logging.basicConfig(level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)-8s] %(message)s",
        datefmt='%a %b %d %Y %H:%M:%S',
        filename='%s/%s.log' % (self.project_dir, self.project_name)
      )
      console = logging.StreamHandler()
      # formatter = logging.Formatter('%(message)s')
      console.setFormatter(logging.Formatter('%(message)s'))
      # Default console logging level
      console.setLevel(logging.WARNING)
      if self.options.debug:
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter('[%(levelname)-8s] %(message)s'))
        logging.getLogger(self.project_name).addHandler(console)
      elif self.options.verbose:
        console.setLevel(logging.INFO)
        logging.getLogger(self.project_name).addHandler(console)
      self.log = logging.getLogger(self.project_name)
      self.log.debug("Initializing BAST %s" % __version__)

    def __init_config(self):
      if not os.path.exists(self.conf):
        print 'Unable to access config file: %s.' % self.conf
        return False
      else:
        from bt import common
        # Read configuration file
        self.config = common.MyConfigParser()
        self.config.read(self.conf)
        return True

    def __init_proc_name(self):
      if sys.platform == 'linux2':
        # Set process name.  Only works on Linux >= 2.1.57.
        try:
          import ctypes
          libc = ctypes.CDLL('libc.so.6')
          libc.prctl(15, 'bast', 0, 0, 0) # 15 = PR_SET_NAME
        except:
          pass

    def __get_class(self, class_name):
      parts = class_name.split('.')
      module = ".".join(parts[:-1])
      m = __import__( module )
      for comp in parts[1:]:
        m = getattr(m, comp)
      return m
    
    def get_conf(self, section, option, default):
      try:
        if self.config.has_section(section):
          if self.config.has_option(section, option):
            return self.config.get(section, option)
      except:
        return default
      else:
        return default
    
    def set_timer(self):
      #from time import time
      pass

    def get_version(self):
      return __version__
    
    def human_size(self, num):
      for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
          return "%3.1f%s" % (num, x)
        num /= 1024.0

    def compress(self, directory):
      self.log.debug('Compressing %s.' % directory)
      import tarfile
      name = directory + '.tar.gz'
      f = tarfile.open(name, 'w:gz')
      f.add(directory)
      f.close()
      shutil.rmtree(directory)
      # Remove latest symlink
      if os.path.islink('latest'):
        os.remove('latest')
      self.log.debug('Creating symbolic link latest -> %s.' % directory)
      os.symlink(name, 'latest')
      return name    
      
    
    def rotate(self, count):
      self.log.debug('Rotating old backups for %s:' % self.project_name)
      l = os.listdir(self.project_dir)
      i = d = 0
      for f in sorted(l, reverse=True):
        if f != 'latest':
          i += 1
          if i > count:
            try:
              os.remove(f)
              d += 1
            except:
              i -= 1
            else:
              self.log.debug('Deleting old backup %s.' % f)              
          else:
            self.log.debug('Keeping backup %s.' % f)
      status = 'Deleted %d of %d old backups.' % (d, (len(l) - 1))
      self.log.debug(status)
      return status
      
    def notify(self, status, report):
      self.log.debug('Sending notifications for %s.' % self.project_name)
      import smtplib
      from email.mime.text import MIMEText
      report.insert(0, 'Backup for %s status is: %s.' % (self.project_name, status))
      report.insert(0, 'Hello!')
      body = "\n".join(report)
      msg = MIMEText(body)
      msg['Subject'] = '[%s - Backup] %s' % (self.project_name, status)
      msg['From'] = self.config.get('BAST', 'mail.username')
      msg['To'] = self.config.get('BAST', 'mail.notify')
      s = smtplib.SMTP(self.config.get('BAST', 'mail.server'), self.config.get('BAST', 'mail.port'))
      s.ehlo()
      if self.config.getboolean('BAST', 'mail.tls', True):
        s.starttls()
      s.ehlo()
      s.login(self.config.get('BAST', 'mail.username'), self.config.get('BAST', 'mail.password'))
      s.sendmail(self.config.get('BAST', 'mail.username'), self.config.get('BAST', 'mail.notify'), msg.as_string())
      s.quit()
    
    def sync(self, backup_file):
      if self.config.get('BAST', 'sync.protocol', 'ftp') == 'ftp':
        self.log.debug('Synchronizing backups for %s over FTP.' % self.project_name)
        from ftplib import FTP
        ftp = FTP(self.config.get('BAST', 'sync.server'))
        if self.config.get('BAST', 'sync.username', None) == None:
          ftp.login()
        else:
          ftp.login(user=self.config.get('BAST', 'sync.username'), passwd=self.config.get('BAST', 'sync.password'))
        f = file(backup_file, 'rb')
        ftp.storbinary('STOR backups/%s--%s' % (self.project_name, backup_file), f)
        ftp.quit()
        