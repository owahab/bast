import os
import sys

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
    
    def to_email(self):
        """
        Handle output to e-mails
        """
        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(self.message)
       
        msg['Subject'] = 'The contents of %s' % textfile
        msg['From'] = me
        msg['To'] = you

        s = smtplib.SMTP()
        s.sendmail(me, [you], msg.as_string())
        s.quit()
