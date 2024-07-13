from fastapi import FastAPI, Response

from podpiped.feedgen import generate_feed
from podpiped.client import PipedApiClient
from podpiped.models import Channel
from podpiped.podcast_builder import PodcastBuilder

app = FastAPI()
client = PipedApiClient()


@app.get("/")
def read_root():
    return {"patterns": [
        "/channel/{channel_id}",
        "/c/{channel_name}",
        "/user/{username}"
    ]}


def handle_channel(channel: Channel) -> Response:
    builder = PodcastBuilder()
    builder.set_channel(channel)
    for stream in channel.relatedStreams:
        try:
            builder.add_stream(client.get_video(stream.video_id))
        except Exception as e:
            print(e)

    content = generate_feed(builder.build())
    return Response(content=content, media_type="application/rss+xml")


@app.get("/channel/{channel_id}")
def read_channel(channel_id: str):
    try:
        channel = client.get_channel_by_id(channel_id)
        return handle_channel(channel)
    except Exception as e:
        print(e)
        return Response(media_type="application/rss+xml", status_code=404)


@app.get("/playlists/{playlist_id}")
def read_channel(playlist_id: str):
    try:
        channel = client.get_playlist_by_id(playlist_id)
        return handle_channel(channel)
    except Exception as e:
        print(e)
        return Response(media_type="application/rss+xml", status_code=404)

@app.get("/c/{channel_name}")
def read_channel(channel_name: str):
    try:
        channel = client.get_channel_by_name(channel_name)
        return handle_channel(channel)
    except Exception as e:
        print(e)
        return Response(media_type="application/rss+xml", status_code=404)


@app.get("/user/{username}")
def read_channel(username: str):
    try:
        channel = client.get_channel_by_user(username)
        return handle_channel(channel)
    except Exception as e:
        print(e)
        return Response(media_type="application/rss+xml", status_code=404)
