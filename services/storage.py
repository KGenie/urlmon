from app_components.service import Service

# TODO While this is a nice database mock for early development, maybe it would
# be a good idea to use some syncronization locks
class StorageService(Service):

    def __init__(self, *args, **kwargs):
        super(StorageService, self).__init__(*args, **kwargs)

        cls = self.__class__
        if not hasattr(cls, 'items'):
            setattr(cls, 'items', [])
            setattr(cls, '_id', 0)
            cls.stub_data()


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
