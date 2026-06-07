class Subscriber:
    def __init__(self,login):
        self.login = login
        self.channels = []

    def __eq__(self, man):
        return man.login == self.login

    def add_channel(self,channel):
        self.channels.append(channel)

    def notify(self,info):
        print(info)

# s1 = Subscriber('Вася')
# s2 = Subscriber('Иван')
# s3 = Subscriber('Петя')
#
# list_subscribers = [s1,s2,s3]
#
# s4 = Subscriber('Иван')
#
# print(s4 in list_subscribers)