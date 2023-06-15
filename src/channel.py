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

    # метод __str__ возвращает название и ссылку на канал
    def __str__(self):
        return f"{self.title} ({self.url})"

    # метод __add__ реализует сложение количества подписчиков
    def __add__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count + other.subscriber_count
        raise ValueError(f"Нельзя сложить экземпляр класса {self.subscriber_count} с экземпляром класса {other.subscriber_count}")

    #метод __sub__реализует вычитание количества подписчиков
    def __sub__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count - other.subscriber_count
        raise ValueError(f"Нельзя вычесть из экземпляра класса {self.subscriber_count} экземпляр класса {other.subscriber_count}")

    # методы __eq__, __lt__, __gt__, __le__, __ge__ реализуют сравнение количества подписчиков
    def __eq__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count == other.subscriber_count
        raise ValueError(f"Нельзя сравнить экземпляр класса {self.subscriber_count} с экземпляром класса {other.subscriber_count}")


    def __lt__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count < other.subscriber_count
        raise ValueError(f"Нельзя сравнить экземпляр класса {self.subscriber_count} с экземпляром класса {other.subscriber_count}")


    def __gt__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count > other.subscriber_count
        raise ValueError(f"Нельзя сравнить экземпляр класса {self.subscriber_count} с экземпляром класса {other.subscriber_count}")


    def __le__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count <= other.subscriber_count
        raise ValueError(f"Нельзя сравнить экземпляр класса {self.subscriber_count} с экземпляром класса {other.subscriber_count}")


    def __ge__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count >= other.subscriber_count
        raise ValueError(f"Нельзя сравнить экземпляр класса {self.subscriber_count} с экземпляром класса {other.subscriber_count}")


    # метод get_service возвращает объект для работы с YouTube API
    @staticmethod
    def get_service():
        return googleapiclient.discovery.build('youtube', 'v3', developerKey="AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI")

    # метод to_json сохраняет в файл значения атрибутов экземпляра Channel
    def to_json(self, filename):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={self.channel_id}&key={self.api_key}'
        response = requests.get(url)
        data = json.loads(response.text)
        print(json.dumps(data, indent=2))

