class VideoItem:
    def __init__(self, title, content):
        self.content = content
        self.title = title

    def __str__(self):
        return f'Видео ролик {self.title}'