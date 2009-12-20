#!/usr/bin/env python

''' This file mainly dispatches calls '''

import sys
import os
import time
from datetime import datetime
from includes import utils
from optparse import OptionParser
from ConfigParser import ConfigParser


def main():
    """ Getting ready... """
    base_path = os.path.dirname(__file__)
    start_time = time.time()
    output = utils.output()
    conf = ConfigParser()
    parser = OptionParser(version="%prog 0.1b", description="BAST (Backup And Synchronization Tools) - Egypt Development Center")
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', help='verbose output [default]', default=True)
    parser.add_option('-q', '--quiet', action='store_false', dest='verbose', help='suppress output', default=True)
    parser.add_option('-c', '--conf', dest='conf', help='read configuration from CONF', metavar='CONF')
    (options, args) = parser.parse_args()

    """ Parsing options... """
    if "config_file" in options.__dict__.items():
        parser.error('Expecting at lease one parameter (try "--help" for help).')
        
    """ Let's get our hands dirty """
    # Read configuration file
    conf.read('%s/%s' % (base_path, options.conf))

    # Dynamically load plugins based on configuration sections
    for section in conf.sections():
        if section != 'general':
            m = get_class("plugins.%s.%s" % (section, section))
            plugin = m()
            plugin.do()

    sys.exit(0)

def get_class(class_name):
    parts = class_name.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

if __name__ == "__main__":
    main()
