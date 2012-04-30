import smtplib, logging, util
from string import Template
from storage import StorageService
from daemons.mailer import DAEMON as mailer_daemon
from models.registration import Registration
from services.notification import NotificationService
from helpers import UrlHelper
from urllib import quote


__logger = logging.getLogger('services.registration')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


u = UrlHelper()

class RegistrationService(StorageService):

   
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
                   
    def pending(self, email):
        return self.session.query(Registration).\
                filter(Registration.email == email).count() > 0
                
    def request_registration(self, user, base_url):
        reg = Registration(user)
        reg.email = user.email
        self.session.add(reg)
        reg_id = reg.reg_id
        my_service = NotificationService
        return NotificationService(my_service).request_registration (reg_id, base_url)

