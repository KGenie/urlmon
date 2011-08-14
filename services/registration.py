import smtplib, datetime
from string import Template
from app_components.service import Service
from daemons.mailer import DAEMON as mailer_daemon
from hashlib import md5
from helpers import UrlHelper
from urllib import quote

_msg_template = Template("""Welcome to the Web Monitor! To activate your account please link on the
following link:
    $activation_link
""")

registration_requests = {}
u = UrlHelper()

class RegistrationService(Service):

    def request_registration(self, user):
        hash = md5()
        hash.update(user.email)
        hash.update(str(datetime.datetime.now()))
        reg_id = hash.hexdigest()
        registration_requests[reg_id] = user
        msg = _msg_template.substitute(
                activation_link=self.reconstruct_url(reg_id))
        subject = 'Activate your account on the Web Monitor'
        mailer_daemon.send((user.email, subject, msg))


    def activate_user(self, reg_id):
        key = None
        user = None
        for k, v in registration_requests.items():
            if k == reg_id:
                key = k
                user = v
                break
        del registration_requests[key]
        return user
            

    def reconstruct_url(self, reg_id):
        environ = self.context.environ
        url = environ['wsgi.url_scheme']+'://'
        if environ.get('HTTP_HOST'):
            url += environ['HTTP_HOST']
        else:
            url += environ['SERVER_NAME']
            if environ['wsgi.url_scheme'] == 'https':
                if environ['SERVER_PORT'] != '443':
                   url += ':' + environ['SERVER_PORT']
            else:
                if environ['SERVER_PORT'] != '80':
                   url += ':' + environ['SERVER_PORT']
        url += u.action(controller='registration', name='confirm_activation',
                reg_id=reg_id)
        return url
