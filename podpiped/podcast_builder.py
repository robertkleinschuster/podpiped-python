from typing import List
from .models import Podcast, Channel, Stream, Episode, VideoStream


class PodcastBuilderException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PodcastBuilder:
    def __init__(self):
        self.__channel: Channel | None = None
        self.__episodes: List[Episode] = []

    def set_channel(self, channel: Channel) -> 'PodcastBuilder':
        self.__channel = channel
        return self

    def add_stream(self, stream: Stream) -> 'PodcastBuilder':
        video_streams: List[VideoStream] = [vs for vs in stream.videoStreams if not vs.videoOnly]

        for video_stream in video_streams:
            title = stream.title
            stream_id = stream.id
            if video_stream.quality:
                title += f' ({video_stream.quality})'
                stream_id += f'-{video_stream.quality}'

            self.__episodes.append(
                Episode(
                    id=stream_id,
                    title=title,
                    description=str(stream.description),
                    duration=int(stream.duration),
                    published=stream.uploadDate,
                    enclosure_url=video_stream.url,
                    enclosure_type=video_stream.mimeType,
                    enclosure_length=int(video_stream.contentLength or 0),
                )
            )

        return self

    @property
    def episode_count(self) -> int:
        return len(self.__episodes)

    def build(self) -> Podcast:
        if self.__channel is None:
            raise PodcastBuilderException("Channel must be set")

        if self.episode_count == 0:
            raise PodcastBuilderException("Stream must be set")

        return Podcast(
            id=self.__channel.id,
            title=self.__channel.name,
            description=self.__channel.description if self.__channel.description else self.__channel.name,
            image=self.__channel.avatarUrl,
            author=self.__channel.name,
            link=f"https://piped.video/channel/{self.__channel.id}",
            episodes=self.__episodes
        )
