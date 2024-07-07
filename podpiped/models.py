from urllib.parse import urlparse, parse_qs
from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class Episode(BaseModel):
    id: HttpUrl
    title: str
    description: str
    enclosure_url: HttpUrl
    enclosure_length: int = -1
    enclosure_type: str = "video/mp4"
    duration: int
    episode_type: str = "full"


class Podcast(BaseModel):
    id: str
    title: str
    link: HttpUrl
    description: str
    language: str = 'en'
    author: str
    explicit: bool = False
    image: Optional[HttpUrl]
    episodes: List[Episode] = []


class VideoStream(BaseModel):
    url: HttpUrl
    mimeType: str
    videoOnly: Optional[bool] = None


class Stream(BaseModel):
    hls: HttpUrl
    title: Optional[str] = None
    description: Optional[str] = None
    uploadDate: Optional[str] = None
    videoStreams: List[VideoStream]
    duration: Optional[int] = None
    uploader: Optional[str] = None
    uploaderUrl: Optional[str] = None


class RelatedStream(BaseModel):
    url: str

    @property
    def video_id(self) -> Optional[str]:
        return parse_qs(urlparse(self.url).query).get("v")[0]


class Channel(BaseModel):
    id: str
    name: str
    relatedStreams: List[RelatedStream]
    description: Optional[str] = None
    avatarUrl: Optional[HttpUrl] = None
