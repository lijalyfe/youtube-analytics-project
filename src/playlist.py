import datetime
import requests

class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title, self.url = self._get_playlist_info()
        self.videos = self._get_videos()

    def _get_playlist_info(self):
        api_key = "AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI"
        url = f"https://www.googleapis.com/youtube/v3/playlists?id={self.playlist_id}&part=snippet&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        playlist = response.json()['items'][0]['snippet']
        return playlist['title'], f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def _get_videos(self):
        api_key = "AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI"
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={self.playlist_id}&part=snippet&maxResults=50&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['items']

    @property
    def total_duration(self):
        total_seconds = 0
        for video in self.videos:
            video_id = video['snippet']['resourceId']['videoId']
            video_response = self._get_video_details(video_id, 'contentDetails')
            duration = video_response['items'][0]['contentDetails']['duration']
            time_parts = duration[2:].split('M')
            minutes = int(time_parts[0]) if time_parts[0] else 0  # Исправление ошибки
            time_parts = time_parts[1].split('S')
            seconds = int(time_parts[0]) if time_parts[0] else 0  # Исправление ошибки
            total_seconds += minutes * 60 + seconds
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        api_key = "AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI"
        max_liked = 0
        most_liked_video_id = ""
        for video in self.videos:
            video_id = video['snippet']['resourceId']['videoId']

            # Получаем статистику видео по его ID
            url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=statistics&key={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            statistics = response.json().get('items')[0].get('statistics')
            likes_count = statistics.get('likeCount') if 'likeCount' in statistics else 0

            print(f'{video.get("snippet", {}).get("title", "NO TITLE")} - likes: {likes_count}')
            if int(likes_count) > max_liked:
                most_liked_video_id = video_id
                max_liked = int(likes_count)
        return f'https://youtu.be/{most_liked_video_id}'

    def _get_video_details(self, video_id, part):
        url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part={part}&key=AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()