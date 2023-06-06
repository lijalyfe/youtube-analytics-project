import requests
import json
import googleapiclient.discovery

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = "AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI"

        # выполняем запрос к YouTube API
        service = Channel.get_service()
        response = service.channels().list(
            part='snippet,statistics',
            id=channel_id
        ).execute()

        # заполняем атрибуты объекта данными из ответа
        item = response['items'][0]
        self.id = item['id']
        self.title = item['snippet']['title']
        self.description = item['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(item['statistics']['subscriberCount'])
        self.video_count = int(item['statistics']['videoCount'])
        self.view_count = int(item['statistics']['viewCount'])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={self.channel_id}&key={self.api_key}'
        response = requests.get(url)
        data = json.loads(response.text)
        print(json.dumps(data, indent=2))

