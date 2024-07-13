import requests_cache
from .models import Channel, Stream


class PipedApiClient:
    session = requests_cache.CachedSession('piped', expire_after=3600)

    def __init__(self, base_url='https://pipedapi.kavin.rocks'):
        self.__base_url = base_url

    def get_video(self, video_id):
        response = self.session.get(f'{self.__base_url}/streams/{video_id}')
        response.raise_for_status()
        return Stream.parse_obj({"id": video_id, **response.json()})

    def get_channel_by_id(self, channel_id):
        response = self.session.get(f'{self.__base_url}/channel/{channel_id}')
        response.raise_for_status()
        return Channel.parse_obj(response.json())

    def get_playlist_by_id(self, playlist_id):
        response = self.session.get(f'{self.__base_url}/playlists/{playlist_id}')
        response.raise_for_status()
        return Channel.parse_obj({"id": playlist_id, **response.json()})

    def get_channel_by_name(self, channel_name):
        response = self.session.get(f'{self.__base_url}/c/{channel_name}')
        response.raise_for_status()
        return Channel.parse_obj(response.json())

    def get_channel_by_user(self, username):
        response = self.session.get(f'{self.__base_url}/user/{username}')
        response.raise_for_status()
        return Channel.parse_obj(response.json())
