from feedgen.feed import FeedGenerator

from podpiped.models import Podcast


def generate_feed(podcast: Podcast) -> str:
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
