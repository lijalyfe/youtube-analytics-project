import os
import datetime
from googleapiclient.discovery import build


class PlayList:
    DEVELOPER_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI")

    def __init__(self, id):
        self.playlist_id = id
        self.title = ""
        self.url = ""
        self.videos = []

        self.initialize_youtube()
        self.fetch_playlist_info()

    def initialize_youtube(self):
        if self.DEVELOPER_KEY:
            self.youtube = build('youtube', 'v3', developerKey=self.DEVELOPER_KEY)
        else:
            raise EnvironmentError("Youtube API key not found.")

    def fetch_playlist_info(self):
        playlist_res = self.youtube.playlists().list(
            part='contentDetails,snippet',
            id=self.playlist_id
        ).execute()
        self.title = playlist_res['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        total = datetime.timedelta(seconds=0)
        for video in self.videos:
            duration = datetime.timedelta(seconds=int(video.duration))
            total += duration
        return total

    def show_best_video(self):
        best_video = max(self.videos, key=lambda x: x.likes)
        return best_video.url

    def fetch_videos(self):
        nextpagetoken = None
        while True:
            plitems_res = self.youtube.playlistItems().list(
                playlistId=self.playlist_id,
                part='contentDetails',
                maxResults=50,
                pageToken=nextpagetoken
            ).execute()
            video_ids = [x['contentDetails']['videoId'] for x in plitems_res['items']]
            videos_res = self.youtube.videos().list(
                part='contentDetails,snippet,statistics',
                id=','.join(video_ids)
            ).execute()
            for video_res in videos_res['items']:
                self.videos.append(PLVideo(video_res['id'], video_res['snippet']['title'],
                                           video_res['contentDetails']['duration'],
                                           int(video_res['statistics']['likeCount']),
                                           f"https://www.youtube.com/watch?v={video_res['id']}"))
            nextpagetoken = plitems_res.get('nextPageToken')
            if not nextpagetoken:
                break