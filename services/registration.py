import smtplib, logging, util
from string import Template
from storage import StorageService
from daemons.mailer import DAEMON as mailer_daemon
from models.registration import Registration
from helpers import UrlHelper
from urllib import quote


__logger = logging.getLogger('services.registration')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


u = UrlHelper()

class RegistrationService(StorageService):

    def request_registration(self, user):
        reg = Registration(user)
        reg.email = user.email
        self.session.add(reg)
        activation_link = self.reconstruct_url(reg.reg_id)
        subject = 'Activate your account on the Web Monitor'
        mailer_daemon.send_template_mail(user.email, subject, 'activate',
                {'activation_link': activation_link})


    def activate_user(self, reg_id):
        ret = None
        reg = self.session.query(Registration).get(reg_id)
        if reg:
            user = reg.user
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            self.session.expunge(user)
            self.session.delete(reg)
            self.session.commit()
            ret = user 
        return ret
                   

    def reconstruct_url(self, reg_id):
        url = util.reconstruct_url(self.context.environ)
        url += u.action(controller='registration', name='confirm_activation',
                reg_id=reg_id)
        return url


    def pending(self, email):
        return self.session.query(Registration).\
                filter(Registration.email == email).count() > 0
