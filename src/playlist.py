import datetime
import requests
from src.video import Video

class PlayList(Video):
    def __init__(self, id):
        self.id = id
        self.title = ""
        self.url = ""



