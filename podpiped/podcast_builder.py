from typing import List
from .models import Podcast, Channel, Stream, Episode


class PodcastBuilderException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PodcastBuilder:
    def __init__(self):
        self.__channel: Channel | None = None
        self.__streams: List[Stream] = []

    def set_channel(self, channel: Channel):
        self.__channel = channel

    def add_stream(self, stream: Stream):
        self.__streams.append(stream)
        return self

    @property
    def episode_count(self) -> int:
        return len(self.__streams)

    def build(self) -> Podcast:
        if self.__channel == None:
            raise PodcastBuilderException("Channel must be set")

        if len(self.__streams) == 0:
            raise PodcastBuilderException("Stream must be set")

        episodes: List[Episode] = list(map(lambda stream: Episode(
            id=stream.hls,
            title=str(stream.title),
            description=str(stream.description),
            duration=int(stream.duration),
            enclosure_url=list(filter(
                lambda video_stream: video_stream.videoOnly == False and video_stream.mimeType == 'video/mp4',
                stream.videoStreams
            ))[0].url
        ), self.__streams))

        return Podcast(
            id=self.__channel.id,
            title=self.__channel.name,
            description=str(self.__channel.description),
            image=self.__channel.avatarUrl,
            author=self.__channel.name,
            link=f"https://piped.video/channel/{self.__channel.id}",
            episodes=episodes
        )
