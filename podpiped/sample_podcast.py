from datetime import datetime

from podpiped.models import Episode, Podcast

sample_episodes = [
    Episode(
        id="https://example.com/episode2",
        title="Episode 2",
        description="This is the second episode.",
        enclosure_url="https://example.com/episode2.mp3",
        enclosure_length=23456789,
        enclosure_type="audio/mpeg",
        duration=120,
        published=datetime.fromisoformat("2024-07-02T15:24:02-07:00"),
        episode_type="full"
    ),
    Episode(
        id="https://example.com/episode1",
        title="Episode 1",
        description="This is the first episode.",
        enclosure_url="https://example.com/episode1.mp3",
        enclosure_length=12345678,
        enclosure_type="audio/mpeg",
        duration=120,
        published=datetime.fromisoformat("2024-07-02T15:24:02-07:00"),
        episode_type="full"
    )
]

sample_podcast = Podcast(
    id="https://example.com/podcast",
    title="My Podcast",
    link="https://example.com",
    description="This is my podcast.",
    language="en",
    author="Author Name",
    explicit=False,
    image="https://example.com/podcast.jpg",
    episodes=sample_episodes
)
