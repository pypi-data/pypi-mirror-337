# TODO: Hacer una clase que maneje todo esto limpiamente.
from const import path_extracted

class PathDownload:
    def __init__(self, *, youtube_id: str):
        self.youtube_id = youtube_id
        self.folder = path_extracted / self.youtube_id
        self.folder.mkdir(exist_ok=True)

        self.audio = self.folder / f"{self.youtube_id}.mp3"
        self.info = self.folder / "info.json"
        self.bass = self.folder / "bass.wav"
        self.drums = self.folder / "drums.wav"
        self.other = self.folder / "other.wav"
        self.piano = self.folder / "piano.wav"
        self.vocals = self.folder / "vocals.wav"
