from models.user import User
from app_components.service import Service

repo = [
        User(email='tap', password='123', roles=['admin']),
        User(email='fred', password='123'),
        User(email='saif', password='123')
        ]

class UserService(Service):


    def authenticate(self, user):
        for u in repo:
            if u.email == user.email:
                if u.password == user.password:
                    return u
                return None


    def get_all(self):
        return repo
