from models.user import User
from app_components.service import Service

repo = [
        User(email='tap', password='123', roles=['admin'])
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

    def add_user(self, user):
        repo.append(user)
