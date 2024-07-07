from feedgen.feed import FeedGenerator
from .models import Podcast, Channel, Stream, Episode


def channel2podcast(channel: Channel):
    return Podcast(
        id=channel.id,
        title=channel.name,
        description=str(channel.description),
        image=channel.avatarUrl,
        author=channel.name,
        link=f"https://piped.video/channel/{channel.id}",
    )


def stream2episode(stream: Stream):
    return Episode(
        id=stream.hls,
        title=str(stream.title),
        description=str(stream.description),
        duration=int(stream.duration),
        enclosure_url=list(filter(
            lambda video_stream: video_stream.videoOnly == False and video_stream.mimeType == 'video/mp4',
            stream.videoStreams
        ))[0].url
    )


def podcast2feed(podcast: Podcast) -> str:
    fg = FeedGenerator()
    fg.generator('podpiped')
    fg.id(str(podcast.id))
    fg.title(podcast.title)
    fg.link(href=str(podcast.link), rel='alternate')
    fg.description(podcast.description)
    fg.language(podcast.language)
    fg.author({'name': podcast.author})
    fg.subtitle(podcast.description)
    fg.load_extension('podcast')
    fg.podcast.itunes_author(podcast.author)
    fg.podcast.itunes_explicit('yes' if podcast.explicit else 'no')
    fg.podcast.itunes_image(str(podcast.image))

    for episode in podcast.episodes:
        fe = fg.add_entry()
        fe.id(str(episode.id))
        fe.title(episode.title)
        fe.description(episode.description)
        fe.enclosure(str(episode.enclosure_url), episode.enclosure_length, episode.enclosure_type)
        fe.podcast.itunes_duration(episode.duration)
        fe.podcast.itunes_episode_type(episode.episode_type)

    return fg.rss_str(pretty=True)
