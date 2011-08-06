from models.user import User
from app_components.service import Service
from storage import StorageService


class UserService(StorageService):

    @classmethod
    def authenticate(cls, user):
        for u in cls.items:
            if u.email == user.email:
                if u.password == user.password:
                    return u
                return None

    @classmethod
    def stub_data(cls):
        cls.insert(User(email='tap', password='123', roles=['admin']))

