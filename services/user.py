from models.user import User
from app_components.service import Service
from storage import StorageService


class UserService(StorageService):

    @classmethod
    def authenticate(cls, email, password):
        for u in cls.items:
            if u.email == email:
                if u.password == password:
                    return u
                return None

    @classmethod
    def stub_data(cls):
        cls.insert(User(email='tpadilha84@gmail.com', first_name='Thiago',
            last_name='Padilha', password='123', roles=['admin']))


    @classmethod
    def exists(cls, email):
        l = list(u for u in cls.items if u.email == email)
        return len(l)
