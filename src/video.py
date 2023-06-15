from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = "AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI"
youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)

class Video:
    def __init__(self, id):
        self.id = id
        self.title = ""
        self.url = ""
        self.views = 0
        self.likes = 0
        try:
            video_request = youtube.videos().list(
                part="snippet, statistics",
                id=self.id
            )
            video_response = video_request.execute()

            if video_response["items"]:
                video = video_response["items"][0]
                self.title = video["snippet"]["title"]
                self.url = f"https://www.youtube.com/watch?v={self.id}"
                self.views = int(video["statistics"]["viewCount"])
                self.likes = int(video["statistics"]["likeCount"])

        except HttpError as e:
            print(f"An error occurred: {e}")


    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, id, playlist_id):
        super().__init__(id)
        self.playlist_id = playlist_id


