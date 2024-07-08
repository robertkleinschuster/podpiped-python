from typing import List
from .models import Podcast, Channel, Stream, Episode, VideoStream


class PodcastBuilderException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PodcastBuilder:
    def __init__(self):
        self.__channel: Channel | None = None
        self.__episodes: List[Episode] = []

    def set_channel(self, channel: Channel):
        self.__channel = channel

    def add_stream(self, stream: Stream):
        video_streams: List[VideoStream] = list(filter(
            lambda vs: vs.videoOnly is False,
            stream.videoStreams
        ))

        for video_stream in video_streams:
            title = stream.title
            id = stream.id
            if video_stream.quality:
                title += f' ({video_stream.quality})'
                id += f'-{video_stream.quality}'

            self.__episodes.append(
                Episode(
                    id=id,
                    title=title,
                    description=str(stream.description),
                    duration=int(stream.duration),
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
            description=str(self.__channel.description),
            image=self.__channel.avatarUrl,
            author=self.__channel.name,
            link=f"https://piped.video/channel/{self.__channel.id}",
            episodes=self.__episodes
        )
