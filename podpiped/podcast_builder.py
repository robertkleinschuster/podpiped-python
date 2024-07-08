from typing import List
from .models import Podcast, Channel, Stream, Episode


class PodcastBuilderException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PodcastBuilder:
    def __init__(self):
        self._channel: Channel | None = None
        self._streams: List[Stream] = []

    def set_channel(self, channel: Channel):
        self._channel = channel

    def add_stream(self, stream: Stream):
        self._streams.append(stream)
        return self

    @property
    def episode_count(self) -> int:
        return len(self._streams)

    def build(self) -> Podcast:
        if self._channel == None:
            raise PodcastBuilderException("Channel must be set")

        if len(self._streams) == 0:
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
        ), self._streams))

        return Podcast(
            id=self._channel.id,
            title=self._channel.name,
            description=str(self._channel.description),
            image=self._channel.avatarUrl,
            author=self._channel.name,
            link=f"https://piped.video/channel/{self._channel.id}",
            episodes=episodes
        )
