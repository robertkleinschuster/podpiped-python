import requests_cache
from .models import Channel, Stream


class PipedApiClient:
    session = requests_cache.CachedSession('piped', expire_after=3600)

    def __init__(self, base_url='https://pipedapi.kavin.rocks'):
        self.__base_url = base_url

    def get_video(self, video_id):
        response = self.session.get(f'{self.__base_url}/streams/{video_id}')
        response.raise_for_status()
        return Stream.parse_obj(response.json())

    def get_channel_info(self, channel_id):
        response = self.session.get(f'{self.__base_url}/channel/{channel_id}')
        response.raise_for_status()
        return Channel.parse_obj(response.json())
