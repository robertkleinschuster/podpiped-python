from pydantic_core._pydantic_core import Url

from podpiped.feedgen import podcast2feed, channel2podcast, stream2episode
from xml.etree import ElementTree as ET

from podpiped.models import Channel, RelatedStream, Stream, VideoStream
from podpiped.sample_podcast import sample_podcast


def test_should_generate_valid_rss_podcast():
    feed = podcast2feed(sample_podcast)
    root = ET.fromstring(feed)

    # Check the root element
    assert root.tag == 'rss'
    assert root.attrib.get('version') == '2.0'

    namespaces = {
        'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'
    }

    channel = root.find('channel')
    assert channel is not None

    # Check the channel elements
    assert channel.find('title').text == 'My Podcast'
    assert channel.find('link').text == 'http://example.com/'
    assert channel.find('description').text == 'This is my podcast.'
    assert channel.find('itunes:author', namespaces).text == 'Author Name'
    assert channel.find('itunes:explicit', namespaces).text == 'no'
    assert channel.find('itunes:image', namespaces).attrib['href'] == 'http://example.com/podcast.jpg'

    # Check the episodes
    items = channel.findall('item')
    assert len(items) == 2

    episode1 = items[0]
    assert episode1.find('title').text == 'Episode 1'
    assert episode1.find('description').text == 'This is the first episode.'
    assert episode1.find('enclosure').attrib['url'] == 'http://example.com/episode1.mp3'
    assert episode1.find('enclosure').attrib['type'] == 'audio/mpeg'
    assert episode1.find('itunes:duration', namespaces).text == "120"
    assert episode1.find('itunes:episodeType', namespaces).text == 'full'

    episode2 = items[1]
    assert episode2.find('title').text == 'Episode 2'
    assert episode2.find('description').text == 'This is the second episode.'
    assert episode2.find('enclosure').attrib['url'] == 'http://example.com/episode2.mp3'
    assert episode2.find('enclosure').attrib['type'] == 'audio/mpeg'
    assert episode2.find('itunes:duration', namespaces).text == "120"
    assert episode2.find('itunes:episodeType', namespaces).text == 'full'

def test_should_build_podcast_from_channel():
    channel = Channel(
        id="UCs6KfncB4OV6Vug4o_bzijg",
        name="My Podcast",
        avatarUrl="https://example.com/podcast.jpg",
        description="This is my podcast.",
        relatedStreams=[
            RelatedStream(
                url="watch?v=a05my9OegME"
            )
        ]
    )

    podcast = channel2podcast(channel)

    assert podcast.id == "UCs6KfncB4OV6Vug4o_bzijg"
    assert podcast.title == "My Podcast"
    assert podcast.description == "This is my podcast."
    assert podcast.link == Url("https://piped.video/channel/UCs6KfncB4OV6Vug4o_bzijg")
    assert podcast.image == Url("https://example.com/podcast.jpg")


def test_should_build_episode_from_stream():
    stream = Stream(
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
    )

    episode = stream2episode(stream)
    assert episode.title == "My Episode"
    assert episode.description == "This is my episode."
    assert episode.id == Url("https://example.com/episode.m3u")
    assert episode.enclosure_url == Url("https://example.com/episode.mp4")
    assert episode.enclosure_type == "video/mp4"
    assert episode.duration == 120
