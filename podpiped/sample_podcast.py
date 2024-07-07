from podpiped.models import Episode, Podcast

sample_episodes = [
    Episode(
        id="http://example.com/episode2",
        title="Episode 2",
        description="This is the second episode.",
        enclosure_url="http://example.com/episode2.mp3",
        enclosure_length=23456789,
        enclosure_type="audio/mpeg",
        duration=120,
        episode_type="full"
    ),
    Episode(
        id="http://example.com/episode1",
        title="Episode 1",
        description="This is the first episode.",
        enclosure_url="http://example.com/episode1.mp3",
        enclosure_length=12345678,
        enclosure_type="audio/mpeg",
        duration=120,
        episode_type="full"
    )
]

sample_podcast = Podcast(
    id="http://example.com/podcast",
    title="My Podcast",
    link="http://example.com",
    description="This is my podcast.",
    language="en",
    author="Author Name",
    explicit=False,
    image="http://example.com/podcast.jpg",
    episodes=sample_episodes
)
