from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = "AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI"
youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)


class Video:
    def __init__(self, id):
        self.id = id
        self.title = None
        self.url = None
        self.views = None
        self.likes = None
        try:
            # инициализируем запрос к API YouTube
            video_request = youtube.videos().list(
                part="snippet, statistics",
                id=self.id
            )
            # отправляем запрос
            video_response = video_request.execute()

            # проверяем есть ли результаты в ответе
            if video_response["items"]:
                # извлекаем информацию о видео
                video = video_response["items"][0]
                # присваиваем нужные свойства объекту
                self.title = video["snippet"]["title"]
                self.url = f"https://www.youtube.com/watch?v={self.id}"
                self.views = int(video["statistics"]["viewCount"])
                self.likes = int(video["statistics"]["likeCount"])

        except HttpError as e:
            # обрабатываем ошибку HTTP
            print(f"An error occurred: {e}")
            self.title = None
            self.url = None
            self.views = None
            self.likes = None


    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, id, playlist_id):
        super().__init__(id)
        self.playlist_id = playlist_id
