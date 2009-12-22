
__version__ = '0.2.0'

import sys
import os
import logging

from bt import common

logger = logging.getLogger(__name__)

class bast(object):
    def __init__(self):
        """
        Initializing
        """
        
        # TODO: make this smarter
        self.set_path()
        
        #self.time_started = time.time()
        self.output = common.output()

        (self.options, self.args) = self.get_options().parse_args()

        """ Parsing options... """
        if "config_file" in self.options.__dict__.items():
            parser.error('Expecting at lease one parameter (try "--help" for help).')
        else:
            self.get_config()
            
        # Dynamically load plugins based on configuration sections
        for section in self.config.sections():
            if section != 'general':
                m = self.get_class("plugins.%s.%s" % (section, section))
                plugin = m()
                plugin.backup(self.config.items(section))

        self._bast = self

    def get_class(self, class_name):
        parts = class_name.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    def get_options(self):
        from optparse import OptionParser
        p = OptionParser(version="%prog 0.1b", description="BAST (Backup And Synchronization Tools) - Egypt Development Center")
        p.add_option('-v', '--verbose', action='store_true', dest='verbose', help='verbose output [default]', default=True)
        p.add_option('-q', '--quiet', action='store_false', dest='verbose', help='suppress output', default=True)
        p.add_option('-c', '--conf', dest='conf', help='read configuration from CONF', metavar='CONF')
        return p

    def get_config(self):
        from ConfigParser import ConfigParser
        # Read configuration file
        self.config = ConfigParser()
        self.config.read(self.options.conf)

    def set_timer(self):
        #from time import time
        pass

    def set_path(self):
        # Find out the location of exaile's working directory, and insert it to sys.path
        basedir = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(os.path.join(basedir, "bast.py")):
            cwd = os.getcwd()
            if os.path.exists(os.path.join(cwd, "bast.py")):
                self.basedir = cwd
        sys.path.insert(0, self.basedir)
        
    def get_version(self):
        return __version__

    def bast():
        return BAST._bast
