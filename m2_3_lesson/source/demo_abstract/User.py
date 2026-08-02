class User:
    users = []
    def __init__(self, login, password):
         self.login = login
         self.password = password

    @classmethod
    def add_admin(cls,user):
        cls.users.append(user)

    def is_access(self):
        for user in User.users:
            if user.password == self.password and user.login == self.login:
                return True
        return False
