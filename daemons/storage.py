import logging, os, fork_vars, glob, sys
from controllable import ControllableDaemon
from app_globals import APP_ROOT

__logger = logging.getLogger('daemons.controllable.storage')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


class Storage(ControllableDaemon):
    
    def __init__(self):
        ControllableDaemon.__init__(self)
        self.module_cache = None


    def process_message(self, message):
        debug('Method call arrived, dispatching it')
        ret = None
        try:
            ret = self.dispatch(*message)
        except Exception as e:
            error('Error ocurred while dispatching method call: %s', e)
        except:
            debug('Method successfully executed, sending back the result')
        return ret


    def init_daemon(self):
        debug('Setting server storage flag...')
        fork_vars.SERVER_STORAGE = True
        self.module_cache = {}
        os.chdir(APP_ROOT)
        debug('Begin to import all services')
        service_names = list(f.replace('.py','').split('/')[1]\
            for f in glob.glob('services/*.py') if\
            '__init__.py' not in f)

        for service_name in service_names:
            module_name = 'services.%s' % service_name
            __import__(module_name, globals=globals(), 
                    fromlist=[service_name])
            self.module_cache[module_name] = sys.modules[module_name]
        debug('Imported all modules successfully')
        os.chdir('/')
            

    def dispatch(self, module_name, class_name, method_name,
            args, kwargs):
        module = self.module_cache[module_name]
        klass = getattr(module, class_name)
        method = getattr(klass, method_name)
        debug('Invoking %s with args %s and kwargs %s' % (method_name, 
            args, kwargs))
        ret = method(*args, **kwargs)
        debug('Method successfully invoked, return value was %s' % ret)
        if hasattr(ret, '__iter__'):
            ret = list(ret)
        return ret
       

DAEMON = Storage()
