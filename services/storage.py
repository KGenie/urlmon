import logging
from app_components.service import Service
from database.sqlalch import Session

__logger = logging.getLogger('services.storage')
debug = __logger.debug
warn = __logger.warn
error = __logger.error
info = __logger.info

  
class StorageService(Service):

    def __init__(self, context, *args, **kwargs):
        self.session = Session()
        self.context = context


    def get_all(self):
        return self.session.query(self.entity).all()
       

    def get(self, id):
        return self.session.query(self.entity).get(id)
       

    def insert(self, item):
        self.session.add(item)
        return item


    def update(self, id, item):
        self.session.merge(item)
        return item
       

    def delete(self, item):
        self.session.delete(item)
