#import logging, signal, urllib2
#from BeautifulSoup import BeautifulSoup
#from multiprocessing import Process, Queue
#from threading import Thread
#
#log = logging.getLogger(__name__)
#
#_queue = None
#_child = None
#
#def run(queue):
#    signal.signal(signal.SIGINT, signal.SIG_IGN)
#    while 1:
#        try:
#        except Exception as e:
#            log.error('Error ocurred: %s', e)
#        except:
#            log.debug('Mail successfully sent!')
#
#
#def initialize():
#    global _queue, _child
#    _queue = Queue()
#    _child = Process(target=run, args=(_queue,)) 
#    _child.daemon = True
#    _child.start()
#
#
#def cleanup():
#    _child.join(0)
#    
#
#def cache_url(url):
#
#def enqueue_mail(to, subject, text, mime='plain'):
#    _queue.put((to, subject, text, mime))
#
#
#def send_mail(to, subject, text, mime):
#    msg = MIMEText(text, mime)
#    msg['Subject'] = subject
#    msg['From'] = _from
#    msg['to'] = to
#
#    conn = smtplib.SMTP(_smtp_server, _port)
#    conn.starttls()
#    conn.ehlo()
#    conn.login(_username, _password)
#    conn.sendmail(_from, [to], msg.as_string())
#    conn.quit()
