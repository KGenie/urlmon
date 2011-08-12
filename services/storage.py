import os, fork_vars, types
from app_components.service import Service, ServiceMetaclass
from multiprocessing.connection import Listener, Client
from threading import Thread, RLock


def generate_client_classmethod_proxy(method_name, socket_path):
    def proxy(cls, *args, **kwargs):
        conn = Client(socket_path, 'AF_UNIX')
        conn.send((method_name, args, kwargs))
        result = conn.recv()
        conn.close()
        return result
    return classmethod(proxy)


def generate_threadsafe_classmethod(method_name, wrapped_func, lock):
    method = wrapped_func.__func__
    def proxy(cls, *args, **kwargs):
        lock.acquire()
        result = method(cls, *args, **kwargs)
        lock.release()
        return result
    return classmethod(proxy)


def serve(cls, listener):
    while 1:
        conn = listener.accept()
        method_name, args, kwargs = conn.recv()
        method = getattr(cls, method_name, None)
        if not method:
            print "unknown method '%s'" % method_name
            continue
        try:
            result = method(*args, **kwargs)
        except Exception, e:
            result = e
        if hasattr(result, '__iter__'):
            result = list(result)
        conn.send(result)
        conn.close()
        

class StorageServiceMetaclass(ServiceMetaclass):
    def __new__(cls, name, bases, attrs):
        socket_dir = fork_vars.STORAGE_SOCKET_DIR
        socket_path = os.path.join(socket_dir, '%sSocket' % name)
        
        is_child = os.path.exists(socket_path)

        method_list = list((k, v) for k, v in attrs.items() if isinstance(v,
            classmethod))

        if is_child:
            for k,v in method_list:
                attrs[k] = generate_client_classmethod_proxy(k, socket_path)
        else:
            lock = RLock()
            for k,v in method_list:
                attrs[k] = generate_threadsafe_classmethod(k, v, lock)

            attrs['_thread_lock'] = lock
            attrs['_id'] = 0
            attrs['items'] = []

        klass = super(StorageServiceMetaclass, cls).__new__(cls, name, bases,
                    attrs)

        if not is_child:
            listener = Listener(socket_path, 'AF_UNIX')
            server_thread = Thread(target=serve, args=(klass, listener))
            server_thread.daemon = True
            server_thread.start()
            setattr(klass, 'server_thread', server_thread)
            klass.stub_data()

        return klass

  
class StorageService(Service):

    __metaclass__ = StorageServiceMetaclass


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
