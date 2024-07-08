from fastapi import FastAPI, Response

from podpiped.feedgen import generate_feed
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
        from podpiped.podcast_builder import PodcastBuilder
        builder = PodcastBuilder()
        builder.set_channel(channel)

        for stream in channel.relatedStreams:
            try:
                builder.add_stream(client.get_video(stream.video_id))
            except Exception as e:
                print(e)
            if builder.episode_count > 5:
                break

        content = generate_feed(builder.build())
        return Response(content=content, media_type="application/rss+xml")
    except Exception as e:
        print(e)
        return Response(media_type="application/rss+xml", status_code=404)
