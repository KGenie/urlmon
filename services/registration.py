import smtplib
from string import Template
from app_components.service import Service
from daemons import mail

_msg_template = Template("""Welcome to the Web Monitor! To activate your account please link on the
following link:
    $activation_link
""")

class RegistrationService(Service):

    def send_activation_link(self, to):
        msg =_msg_template.substitute(from=_from, to=to,
                activation_link=activation_link)
        subject = 'Activate your account on the Web Monitor'
        mail.enqueue_mail(to, subject, msg)
