class Video:
    def __init__(self, id, title, url, views, likes):
        self.id = id
        self.title = title
        self.url = url
        self.views = views
        self.likes = likes

class PLVideo(Video):
    def __init__(self, id, title, url, views, likes, playlist_id):
        super().__init__(id, title, url, views, likes)
        self.playlist_id = playlist_id
