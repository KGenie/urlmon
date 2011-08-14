import os, fork_vars, logging
from app_components.service import Service, ServiceMetaclass
from multiprocessing.connection import Client
from daemons.storage import DAEMON as storage_daemon

__logger = logging.getLogger('services.storage')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info


def generate_client_classmethod_proxy(method_name, socket_path):
    def proxy(cls, *args, **kwargs):
        module_name = cls.__module__
        class_name = cls.__name__
        result = storage_daemon.send((module_name, class_name, 
            method_name, args, kwargs), get_response=True)
        debug('RESULT was %s' % result)
        return result
    return classmethod(proxy)


def proxy_class_methods(attrs):
    socket_dir = fork_vars.IPC_SOCKET_DIR
    socket_path = os.path.join(socket_dir, 'storage.socket')

    method_list = list((k, v) for k, v in attrs.items() if \
            isinstance(v, classmethod))

    for k,v in method_list:
        attrs[k] = generate_client_classmethod_proxy(k, socket_path)


class ServerStorageServiceMetaclass(ServiceMetaclass):

    def __new__(cls, name, bases, attrs):
        debug('Creating server DAO %s' % os.getpid())
        attrs['_id'] = 0
        attrs['items'] = []
        
        klass = super(ServerStorageServiceMetaclass, cls).__new__(cls, 
                    name, bases, attrs)
        klass.stub_data()
        debug('Server DAO %s successfully created' % name)
           
        return klass



class ClientStorageServiceMetaclass(ServiceMetaclass):

    def __new__(cls, name, bases, attrs):
        debug('Creating client DAO %s' % name)
        proxy_class_methods(attrs)
        klass = super(ClientStorageServiceMetaclass, cls).__new__(cls, 
                    name, bases, attrs)
        debug('Client DAO %s successfully created' % name)
        return klass


  
class StorageService(Service):

    if fork_vars.SERVER_STORAGE == True:
        debug('Setting to server metaclass')
        __metaclass__  = ServerStorageServiceMetaclass
    else:
        debug('Setting to client metaclass')
        __metaclass__ = ClientStorageServiceMetaclass



    @classmethod
    def next_id(cls):
        cls._id += 1
        return cls._id


    @classmethod
    def stub_data(cls):
        pass


    @classmethod
    def get_all(cls):
        return iter(cls.items)
       

    @classmethod
    def get_all_by_user(cls, user):
        all = cls.get_all()
        return (t for t in all if t.user_id == user.id)


    @classmethod
    def get(cls, id):
        id = int(id)
        for item in cls.items:
            if item.id == id:
                return item
        return None
        

    @classmethod
    def insert(cls, item):
        id = cls.next_id()
        item.id = id
        cls.items.append(item)
        return item


    @classmethod
    def update(cls, id, item):
        id = int(id)
        i = 0
        for t in cls.items:
            if t.id == id:
                break
            i = i + 1
        if i < len(cls.items):
            item.id = id
            cls.items[i] = item
        return item


    @classmethod
    def delete(cls, id):
        id = int(id)
        ret = None
        for item in cls.items:
            if item.id == id:
                ret = item
                break
        if ret:
            cls.items.remove(ret)
        return ret
