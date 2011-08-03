from models.user import User
from app_components.service import Service

repo = [
        User('tap', '123', 'Thiago de Arruda', roles=['admin']),
        User('fred', '123', 'Frederic Bazin'),
        User('saif', '123', 'Saif Bonar')
        ]

class UserService(Service):


    def authenticate(self, user):
        for u in repo:
            if u.username == user.username:
                if u.password == user.password:
                    return u
                return None
