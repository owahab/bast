import os
import sys
from ConfigParser import RawConfigParser

class output:
    """
    Send a message to stdin, email, etc...
    """
    def to_shell(self):
        """
        Handle coloured output to BASH
        """
        colors = {'bold': '\x1b[1m', 
                  'normal':'\x1b[0m',
                  'blue':'\x1b[34m',
                  'green':'\x1b[32m',
                  'red':'\x1b[31m',
                  'cyan':'\x1b[36m'
                  }
        if (os.environ['SHELL'] != '/bin/bash' or (self.params['bold'] == False and self.params['color'] == '')):
            sys.stdout.writelines(self.message)
        else:
            text = ""
            if "bold" in self.params and self.params['bold'] == True:
                text += "%(bold)s" % colors
            for key in colors:
                if key == color:
                    text += colors[key]
            text += self.message
            text += "%(normal)s" % colors
            sys.stderr.writelines(text)
        return 0
        

class MyConfigParser(RawConfigParser):
  def __init__(self):
  		RawConfigParser.__init__(self)
  
  def get(self, section, option, default = None):
    value = default
    try:
      if RawConfigParser.has_section(self, section):
        if RawConfigParser.has_option(self, section, option):
          value = RawConfigParser.get(self, section, option)
    except:
      value = default
    return value

  def getboolean(self, section, option, default):
    value = default
    try:
      if RawConfigParser.has_section(self, section):
        if RawConfigParser.has_option(self, section, option):
          value = RawConfigParser.getboolean(self, section, option)
    except:
      value = default
    return value

  def getint(self, section, option, default):
    value = default
    try:
      if RawConfigParser.has_section(self, section):
        if RawConfigParser.has_option(self, section, option):
          value = RawConfigParser.getint(self, section, option)
    except:
      value = default
    return value