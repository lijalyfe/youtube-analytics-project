import requests

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = "AIzaSyBTN9KzMhMCpC1S15uq6O9O7-xLv45AwgI"


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        pass
