import smtplib, logging, signal
from multiprocessing import Process, Queue
from email.mime.text import MIMEText

log = logging.getLogger(__name__)


_from = 'thiago.arruda@live.com'
_smtp_server = 'smtp.live.com'
_port = 587
_username = 'thiago.arruda@live.com'
_password = 'ark123ark'
_queue = None
_child = None

def run(queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    while 1:
        log.debug('Waiting for mail to arrive...')
        msg = queue.get()
        log.debug('Mail arrived, sending it...')
        try:
            send_mail(*msg)
        except Exception as e:
            log.error('Error ocurred while sending mail: %s', e)
        except:
            log.debug('Mail successfully sent!')


def initialize():
    global _queue, _child
    _queue = Queue()
    _child = Process(target=run, args=(_queue,)) 
    _child.daemon = True
    _child.start()


def cleanup():
    _child.join(0)
    

def enqueue_mail(to, subject, text, mime='plain'):
    _queue.put((to, subject, text, mime))


def send_mail(to, subject, text, mime):
    msg = MIMEText(text, mime)
    msg['Subject'] = subject
    msg['From'] = _from
    msg['to'] = to

    conn = smtplib.SMTP(_smtp_server, _port)
    conn.starttls()
    conn.ehlo()
    conn.login(_username, _password)
    conn.sendmail(_from, [to], msg.as_string())
    conn.quit()
