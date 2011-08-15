import smtplib, logging
from controllable import ControllableDaemon
from email.mime.text import MIMEText

__logger = logging.getLogger('daemons.controllable.mailer')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


class Mailer(ControllableDaemon):

    def __init__(self, 
            sender='thiago.arruda@live.com',
            smtp_server='smtp.live.com',
            port=587,
            username='thiago.arruda@live.com',
            password='ark123ark'):
        ControllableDaemon.__init__(self)
        self.sender = sender
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password


    def process_message(self, message):
        debug('Mail arrived, trying to send it...')
        try:
            self.__sendmail(*message)
        except Exception as e:
            error('Error ocurred while sending mail: %s', e)
        else:
            debug('Mail successfully sent!')


    def __sendmail(self, to, subject, text, mime='plain', charset='utf-8'):
        msg = MIMEText(text, mime, charset)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['to'] = to

        conn = smtplib.SMTP(self.smtp_server, self.port)
        conn.starttls()
        conn.ehlo()
        conn.login(self.username, self.password)
        conn.sendmail(self.sender, [to], msg.as_string())
        conn.quit()


    def sendmail(self, email, subject, msg):
        self.send((email, subject, msg))

DAEMON = Mailer()
