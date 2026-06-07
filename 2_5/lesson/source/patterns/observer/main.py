from patterns.observer.Subscriber import Subscriber
from patterns.observer.VideoItem import VideoItem
from patterns.observer.YoutubeChannel import YouTubeChannel

item1 = VideoItem('Основы Python,','Контент1')
item2 = VideoItem('Основы JS,','Контент2')
item3 = VideoItem('Основы Apache Kafka,','Контент3')

channel = YouTubeChannel('Блог программиста')

channel.add_item(item1)
channel.add_item(item2)
channel.add_item(item3)

subscriber1 = Subscriber('Иван')
subscriber2 = Subscriber('Петр')
subscriber3 = Subscriber('Анна')

channel.add_subscriber(subscriber1)
channel.add_subscriber(subscriber2)
channel.add_subscriber(subscriber3)

item4 = VideoItem('Python в м/с архитектуре','Описание ролика...')
channel.add_item(item4)

channel.unsubscribe(subscriber2)

print('Оставшиеся подписчики')
for subscriber in channel.subscribers:
    print(subscriber.login)