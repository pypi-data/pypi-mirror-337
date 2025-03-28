import json
from pathlib import Path
from typing import Dict, List
from typing_extensions import TypedDict
from youtubesearchpython import ChannelsSearch, playlist_from_channel_id
from urllib.parse import urlparse, parse_qs
from yt_dlp import YoutubeDL

from .config import Config


# === Typages ===


class ChannelInfo(TypedDict):
    title: str
    handle: str
    id: str


class PlaylistInfo(TypedDict):
    title: str
    link: str
    id_playlist: str
    video_count: str
    thumbnail: str


class VideoInfos(TypedDict):
    id: str
    title: str
    url: str
    full_url: str
    duration: str
    thumbnail: str
    channel: str
    order: int


class YoutubeCache(TypedDict):
    lislamsimplement: ChannelInfo
    larabesimplement: ChannelInfo
    lecoransimplement: ChannelInfo


# === Classe principale ===


class YoutubeServices:
    def __init__(self):
        self.handles = Config.handles_yt()
        self.path = Path(__file__).parent / "data" / "cacheYT.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.__setup_cache()

        self.__cache: YoutubeCache = self.__read_cache()

    def __setup_channels(self) -> YoutubeCache:
        data: Dict[str, ChannelInfo] = {}
        for k, v in self.handles._asdict().items():
            search = ChannelsSearch(v, limit=1, language="fr", region="FR")
            result = search.result()
            if result["result"]:
                channel = result["result"][0]
                data[k] = {
                    "title": channel["title"],
                    "handle": v,
                    "id": channel["id"],
                }
            else:
                raise ValueError(f"Aucun résultat trouvé pour le handle {v}")

        return data  # type: ignore

    def __setup_cache(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.__setup_channels(), f, ensure_ascii=False, indent=4)

    def __read_cache(self) -> YoutubeCache:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def refresh_cache(self) -> None:
        """Force la mise à jour du cache."""
        self.__setup_cache()
        self.__cache = self.__read_cache()

    @property
    def channels(self) -> YoutubeCache:
        return self.__cache

    def _get_channel_by_handle(self, handle: str) -> ChannelInfo:
        for ch in self.channels.values():
            if ch["handle"] == handle:
                return ch
        raise ValueError(f"Handle '{handle}' introuvable dans le cache.")

    def format_url(self, handle: str) -> str:
        channel = self._get_channel_by_handle(handle)
        return f"https://www.youtube.com/{channel['handle']}"

    def playlists(self, handle: str) -> List[PlaylistInfo]:
        url = self.format_url(handle)
        ydl_options = {"extract_flat": True, "force_generic_extractor": True}
        with YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(f"{url}/playlists", download=False)
            playlists = info.get("entries", [])
            return [
                PlaylistInfo(
                    title=pl.get("title", ""),
                    link=pl.get("url", ""),
                    id_playlist=self.extract_playlist_id(pl.get("url", "")),
                    video_count=str(pl.get("video_count", "0")),
                    thumbnail=pl.get("thumbnails", [{}])[0].get("url", ""),
                )
                for pl in playlists
                if pl.get("url")
            ]

    def extract_playlist_id(self, playlist_url: str) -> str:
        query = urlparse(playlist_url).query
        params = parse_qs(query)
        return params.get("list", [""])[0]

    def is_valid_playlist(self, playlist_id: str) -> bool:
        url = playlist_from_channel_id(playlist_id)
        try:
            with YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return bool(info and info.get("entries"))
        except Exception:
            return False

    def videos_from_playlist(self, playlist_id: str) -> List[VideoInfos]:
        if not self.is_valid_playlist(playlist_id):
            raise ValueError("Playlist non trouvée ou invalide")

        url = playlist_from_channel_id(playlist_id)
        ydl_options = {"quiet": True, "extract_flat": False}

        with YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            videos = info.get("entries", [])
            return [
                {
                    "id": v.get("id", ""),
                    "title": v.get("title", ""),
                    "url": f"https://www.youtube.com/watch?v={v.get('id')}",
                    "full_url": f"https://www.youtube.com/watch?v={v.get('id')}&list={playlist_id}",
                    "duration": v.get("duration_string") or v.get("duration") or "",
                    "thumbnail": (v.get("thumbnails") or [{}])[-1].get("url", ""),
                    "channel": v.get("channel", ""),
                    "order": idx + 1,
                }
                for idx, v in enumerate(videos)
                if v.get("id")
            ]
