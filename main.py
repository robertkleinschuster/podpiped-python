from fastapi import FastAPI, Response

from podpiped.feedgen import podcast2feed, channel2podcast, stream2episode
from podpiped.sample_podcast import sample_podcast
from podpiped.client import PipedApiClient

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/channel/{channel_id}")
def read_channel(channel_id: str):
    client = PipedApiClient()
    try:
        channel = client.get_channel_info(channel_id)
        podcast = channel2podcast(channel)

        episodes = []
        for stream in channel.relatedStreams:
            try:
                episodes.append(stream2episode(client.get_video(stream.video_id)))
                if len(episodes) > 5:
                    break
            except Exception as e:
                print(e)

        podcast.episodes = episodes

        content = podcast2feed(podcast)
        return Response(content=content, media_type="application/rss+xml")
    except Exception as e:
        print(e)
        return Response(media_type="application/rss+xml", status_code=404)
