class YouTubeChannel:
    def __init__(self,title_channel):
        self.title_channel = title_channel
        self.items = []
        self.subscribers = []

    def add_subscriber(self,subscriber):
        self.subscribers.append(subscriber) #добавление подписчика на канал
        subscriber.add_channel(self.title_channel) #добавление подписчику нашего канала в его список каналов
        print(f'{subscriber.login} успешно добавлен в подписчики канала {self.title_channel}')

    def unsubscribe(self,subscriber):
        size = len(self.subscribers)

        if subscriber in self.subscribers:
            subscriber.channels.remove(self.title_channel)
            self.subscribers.remove(subscriber)
        if len(self.subscribers) == size - 1:
            print('Подписчик',subscriber.login,'успешно удален с канала',self.title_channel)
            return
        print("Ошибка при удалении подписчика с канала!")

    def add_item(self,item):
        self.items.append(item)
        if self.subscribers:
            for subscriber in self.subscribers:
                subscriber.notify(f'На канале {self.title_channel} вышел ролик {item.title}')
