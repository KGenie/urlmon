import smtplib, logging, app_globals, os
from traceback import format_exc
from controllable import ControllableDaemon
from email.mime.text import MIMEText
from helpers import HtmlHelper, UrlHelper
from jinja2 import Environment, FileSystemLoader

__logger = logging.getLogger('daemons.controllable.mailer')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info




def make_jinja_email_environment():
    ret = Environment(loader=FileSystemLoader(
        os.path.join(app_globals.APP_ROOT, 'email_templates')))
    ret.globals['h'] = HtmlHelper()
    ret.globals['u'] = UrlHelper()
    return ret


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
            method = message[0]
            args = message[1:]
            debug('Method is %s' % method)
            if method == 'PLAIN':
                self.__send_mail(*args)
            elif method == 'TEMPLATE':
                self.__send_template_mail(*args)
            else:
                error('Unknown method: %s')
        except Exception as e:
            error('Error ocurred while sending mail: %s', format_exc(e))
        else:
            debug('Mail successfully sent!')


    def __send_mail(self, to, subject, text, mime='plain', charset='utf-8'):
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


    def __send_template_mail(self, to, subject, template_name, 
            template_context, mime='html', charset='utf-8'):

        # Normalize template context
        for k, v in template_context.items():
            if isinstance(v, str):
                template_context[k] = v.decode('utf-8')


        env = app_globals.JINJA_EMAIL_ENV
        templ = env.get_template(template_name + '.jinja2')

        text = templ.render(template_context)


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


    def send_mail(self, email, subject, msg):
        self.send(('PLAIN', email, subject, msg))


    def send_template_mail(self, to, subject, template_name, 
            template_context):
        self.send(('TEMPLATE', to, subject, template_name, 
            template_context))



DAEMON = Mailer()
app_globals.JINJA_EMAIL_ENV = make_jinja_email_environment()
