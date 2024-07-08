from pydantic_core._pydantic_core import Url
from podpiped.models import Channel, RelatedStream, Stream, VideoStream
from podpiped.podcast_builder import PodcastBuilder, PodcastBuilderException
import pytest


def test_should_raise_error_if_no_channel_was_set():
    builder = PodcastBuilder()
    with pytest.raises(PodcastBuilderException, match='Channel must be set'):
        builder.build()


def test_should_raise_error_if_no_streams_were_added():
    builder = PodcastBuilder()
    builder.set_channel(Channel(
        id="UCs6KfncB4OV6Vug4o_bzijg",
        name="My Podcast",
        avatarUrl="https://example.com/podcast.jpg",
        description="This is my podcast.",
        relatedStreams=[
            RelatedStream(
                url="watch?v=a05my9OegME"
            )
        ]
    ))
    with pytest.raises(PodcastBuilderException, match='Stream must be set'):
        builder.build()


def test_should_build_podcast_from_channel_and_streams():
    builder = PodcastBuilder()
    builder.set_channel(Channel(
        id="UCs6KfncB4OV6Vug4o_bzijg",
        name="My Podcast",
        avatarUrl="https://example.com/podcast.jpg",
        description="This is my podcast.",
        relatedStreams=[
            RelatedStream(
                url="watch?v=a05my9OegME"
            )
        ]
    ))
    builder.add_stream(Stream(
        title="My Episode",
        description="This is my episode.",
        hls="https://example.com/episode.m3u",
        duration=120,
        uploadDate="2024-07-02T15:24:02-07:00",
        videoStreams=[
            VideoStream(
                url="https://example.com/episode_video_only.mp4",
                mimeType="video/mp4",
                videoOnly=True
            ),
            VideoStream(
                url="https://example.com/episode.mp4",
                mimeType="video/mp4",
                videoOnly=False
            )
        ]
    ))

    builder.add_stream(Stream(
        title="My Episode 2",
        description="This is my second episode.",
        hls="https://example.com/episode2.m3u",
        duration=240,
        uploadDate="2024-07-03T15:24:02-07:00",
        videoStreams=[
            VideoStream(
                url="https://example.com/episode2.mp4",
                mimeType="video/mp4",
                videoOnly=False
            ),
            VideoStream(
                url="https://example.com/episode2_video_only.mp4",
                mimeType="video/mp4",
                videoOnly=True
            )
        ]
    ))

    podcast = builder.build()

    assert podcast.id == "UCs6KfncB4OV6Vug4o_bzijg"
    assert podcast.title == "My Podcast"
    assert podcast.description == "This is my podcast."
    assert podcast.link == Url("https://piped.video/channel/UCs6KfncB4OV6Vug4o_bzijg")
    assert podcast.image == Url("https://example.com/podcast.jpg")

    episode1 = podcast.episodes[0]
    episode2 = podcast.episodes[1]

    assert episode1.title == "My Episode"
    assert episode1.description == "This is my episode."
    assert episode1.id == Url("https://example.com/episode.m3u")
    assert episode1.enclosure_url == Url("https://example.com/episode.mp4")
    assert episode1.enclosure_type == "video/mp4"
    assert episode1.duration == 120

    assert episode2.title == "My Episode 2"
    assert episode2.description == "This is my second episode."
    assert episode2.id == Url("https://example.com/episode2.m3u")
    assert episode2.enclosure_url == Url("https://example.com/episode2.mp4")
    assert episode2.enclosure_type == "video/mp4"
    assert episode2.duration == 240
