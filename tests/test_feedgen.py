from podpiped.feedgen import generate_feed
from xml.etree import ElementTree as ET

from podpiped.sample_podcast import sample_podcast


def test_should_generate_valid_rss_podcast():
    feed = generate_feed(sample_podcast)
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

    episode2 = items[0]
    assert episode2.find('title').text == 'Episode 2'
    assert episode2.find('description').text == 'This is the second episode.'
    assert episode2.find('enclosure').attrib['url'] == 'http://example.com/episode2.mp3'
    assert episode2.find('enclosure').attrib['type'] == 'audio/mpeg'
    assert episode2.find('itunes:duration', namespaces).text == "120"
    assert episode2.find('itunes:episodeType', namespaces).text == 'full'

    episode1 = items[1]
    assert episode1.find('title').text == 'Episode 1'
    assert episode1.find('description').text == 'This is the first episode.'
    assert episode1.find('enclosure').attrib['url'] == 'http://example.com/episode1.mp3'
    assert episode1.find('enclosure').attrib['type'] == 'audio/mpeg'
    assert episode1.find('itunes:duration', namespaces).text == "120"
    assert episode1.find('itunes:episodeType', namespaces).text == 'full'
