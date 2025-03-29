import json
from pathlib import Path
from typing import Dict, List, cast
from typing_extensions import TypedDict
from youtubesearchpython import ChannelsSearch, PlaylistsSearch
from urllib.parse import urlparse, parse_qs
from pytube import Playlist, YouTube
from concurrent.futures import ThreadPoolExecutor, as_completed

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


class VideoInfo(TypedDict):
    title: str
    url: str
    full_url: str
    order: int
    duration: str
    thumbnail: str


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
            cache: YoutubeCache = cast(YoutubeCache, json.load(f))
        return cache

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
        """Recherche les playlists d'une chaîne via son handle YouTube."""
        channel = self._get_channel_by_handle(handle)
        query = f"{channel['title']} playlist"
        search = PlaylistsSearch(query, limit=20)
        results = search.result().get("result", [])

        playlists: List[PlaylistInfo] = []
        for item in results:
            playlist_url = item.get("link", "")
            playlist_id = self.extract_playlist_id(playlist_url)
            playlists.append(
                PlaylistInfo(
                    title=item.get("title", ""),
                    link=playlist_url,
                    id_playlist=playlist_id,
                    video_count=str(item.get("videoCount", "0")),
                    thumbnail=item.get("thumbnails", [{}])[0].get("url", ""),
                )
            )
        return playlists

    def extract_playlist_id(self, playlist_url: str) -> str:
        query = urlparse(playlist_url).query
        params = parse_qs(query)
        return params.get("list", [""])[0]

    def is_valid_playlist(self, playlist_id: str) -> bool:
        url = self.format_url_playlist(playlist_id)
        try:
            playlist = Playlist(url)
            return len(playlist.video_urls) > 0
        except Exception:
            return False

    def format_url_playlist(self, id_playlist: str) -> str:
        return f"https://www.youtube.com/playlist?list={id_playlist}"

    def videos(self, playlist_id: str) -> List[VideoInfo]:
        if not self.is_valid_playlist(playlist_id):
            raise ValueError("ID de la playlist invalide")

        url = self.format_url_playlist(playlist_id)
        playlist = Playlist(url)

        def process_video(idx_url):
            idx, video_url = idx_url
            try:
                yt = YouTube(video_url)
                return VideoInfo(
                    title=yt.title,
                    url=yt.watch_url,
                    full_url=f"{yt.watch_url}&list={playlist_id}",
                    order=idx + 1,
                    duration=f"{yt.length // 60} min {yt.length % 60} sec",
                    thumbnail=yt.thumbnail_url,
                )
            except Exception as e:
                print(f"[ERREUR] Impossible de traiter la vidéo {video_url} : {e}")
                return None

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(process_video, pair)
                for pair in enumerate(playlist.video_urls)
            ]
            results = [
                res
                for res in (future.result() for future in as_completed(futures))
                if res
            ]

        return sorted(results, key=lambda v: v["order"])
