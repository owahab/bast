
__version__ = '0.2.0'

import sys
import os
import logging
from threading import Thread

from bt import common

log = logging.getLogger(__name__)

class bast(object):
    def __init__(self):
        """
        Initializing
        """
        self.__init_proc_name()

        self.__init_options()

        # Logging
        self.__init_logging()
        log.info("Initializing BAST %s" % __version__)
        
        # TODO: make this path thingy a little smarter
        self.__init_path()

        #self.time_started = time.time()
        #self.output = common.output()
        
        self.get_config()

        # Dynamically load plugins based on configuration sections
        for section in self.config.sections():
            if section != 'general':
                m = self.__get_class("plugins.%s.%s" % (section, section))
                p = m()
                Thread(target=p.backup, args=(self.config.items(section)), name=section).start()
                #p.start()

        self._bast = self


    def __init_path(self):
        log.info('Initializing path settings...')
        # Find out the location of bast's working directory, and insert it to sys.path
        basedir = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(os.path.join(basedir, "bast.py")):
            cwd = os.getcwd()
            if os.path.exists(os.path.join(cwd, "bast.py")):
                self.basedir = cwd
        sys.path.insert(0, self.basedir)

    def __init_options(self):
        log.info('Initializing option parser...')
        from optparse import OptionParser
        parser = OptionParser(version="%prog 0.1b",
                                   description="BAST (Backup And Synchronization Tools) - Egypt Development Center",
                                   usage="%prog [options] <conf-file>")
        parser.add_option('-v', '--verbose', action='store_true', dest='verbose', help='verbose output', default=False)
        parser.add_option('-d', '--debug', action='store_true', dest='debug', help='debug', default=False)

        (self.options, self.args) = parser.parse_args()
        if not len(self.args):
            log.error('Expecting a configuration file to be given (try "--help" for help).')
            parser.error('Expecting a configuration file to be given (try "--help" for help).')
        else:
            self.conf = self.args[0]
        
    def __init_logging(self):
        console_format = "%(levelname)-8s: %(message)s"
        log_level = logging.WARNING
        if self.options.verbose:
            log_level = logging.INFO
        if self.options.debug:
            log_level = logging.DEBUG
            console_format += " (%(name)s)"
            
        # Console logging
        logging.basicConfig(level=log_level, format=console_format)

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

    def get_config(self):
        log.info("Loading configuration file %s..." % self.conf)
        from ConfigParser import ConfigParser
        # Read configuration file
        self.config = ConfigParser()
        self.config.read(self.conf)

    def set_timer(self):
        #from time import time
        pass

    def get_version(self):
        return __version__

    def bast():
        return BAST._bast
