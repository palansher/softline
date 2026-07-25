class AdminUsers:
    def __init__(self):
        self.users = []

    def add_user(self,user):
        self.users.append(user)

    def remove_user(self,user):
        self.users.remove(user)