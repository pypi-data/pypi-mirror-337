"""
- TODO: Averiguar si puedo controlar el suffix de una forma cómoda.
"""
from typing import Optional, List
from urllib.parse import urlparse
import logging
import json
import re

from yt_dlp import YoutubeDL
from src.path_download import PathDownload

T_YoutubeId = str
INDENT = 4
logger = logging.getLogger(__name__)


def youtube_id_from_url(*, url: str) -> Optional[T_YoutubeId]:
    # Validar que la URL es de YouTube (sin importar el esquema http/https)
    parsed_url = urlparse(url)
    if parsed_url.netloc not in ['www.youtube.com', 'youtube.com']:
        return None

    # Buscar el ID del video en la URL
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def youtube_ids_from_urls(*, urls: List[str]) -> List[tuple[Optional[T_YoutubeId], str]]:
    return [(youtube_id_from_url(url=url), url) for url in urls]


def serialize_yt_info(yt_info: dict) -> dict:
    yt_info_cleaned = {}

    for key, value in yt_info.items():
        try:
            # Intenta serializar el valor para ver si es serializable
            json.dumps(value)
            yt_info_cleaned[key] = value
        except (TypeError, ValueError):
            # Si el valor no es serializable, lo omite
            continue

    return yt_info_cleaned


class Youtube:
    def __init__(self, *, youtube_id: str, path_download: PathDownload):
        self.youtube_id: T_YoutubeId = youtube_id
        self.path_download = path_download

        # Referencia absoluta extraída con la api.
        #self.path_audio: Optional[Path] = None

    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.youtube_id}"

    def extract_info(self, *, ydl: YoutubeDL) -> dict:
        yt_info = ydl.extract_info(self.url, download=True)
        
        # Filtra los campos no serializables
        yt_info = serialize_yt_info(yt_info)
        
        for field_to_delete in self.info_fields_to_delete():
            yt_info.pop(field_to_delete)
        
        #self.path_audio = Path(yt_info["requested_downloads"][0]["filepath"])

        with open(self.path_download.info, "w") as f:
            json.dump(yt_info, f, indent=INDENT)

    def download_audio(self) -> None:
        """
        - Crea un folder en `path_out/<youtube_id>/<youtube_id>.mp3`.
        """
        logger.info(f"- Download audio - youtube_id={self.youtube_id}")
        with YoutubeDL(self.get_options_youtube_dl()) as ydl:
            yt_info = self.extract_info(ydl=ydl)
            # --> TODO: Se puede seguir procesando el yt_info.

    def get_options_youtube_dl(self) -> dict:
        return {
            "format": "bestaudio/best",
            "outtmpl": str(self.path_download.folder / f"{self.youtube_id}.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }
            ]
        }

    @staticmethod
    def info_fields_to_delete() -> List[str]:
        """ Campos para borrar del info, son pesados, ver si sirve el dato."""
        return [
            "formats",
            "thumbnails",
            "heatmap"       #TODO: heatmap -> Graficar esto. Creo que es la forma de las ondas.
        ]
