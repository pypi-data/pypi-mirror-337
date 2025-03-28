from pathlib import Path
from typing import Optional

from .metasurahs import MetaSurahs, LanguageOptions
from .meta_quran_reader import MetaQuranReader
from .memory_quran import MemoryQuran
from .yt_services import YoutubeServices
from .config import Config


class MyDeen:
    """
    Point d'entrée principal du package `mydeen`.
    Fournit l'accès aux différents services liés au Coran, YouTube et mémorisation.
    """

    def __init__(
        self,
        language: Optional[LanguageOptions] = None,
        eager: bool = False,  # 🆕 Option d'initialisation anticipée
    ) -> None:
        path = Path(__file__).parent / "data"
        path.mkdir(parents=True, exist_ok=True)
        self.path_database = path.as_posix()

        self.__language = (
            MetaSurahs(self.path_database, language).language if language else None
        )
        self.__youtube_instance: Optional[YoutubeServices] = None

        self.setup_all(eager=eager)

    @property
    def language(self) -> Optional[LanguageOptions]:
        return self.__language

    def config_url(self) -> Config:
        """Retourne la configuration des URLs de ressources utilisées."""
        return Config()

    def meta_surahs(self, language: Optional[LanguageOptions] = None) -> MetaSurahs:
        """Retourne les métadonnées des sourates du Coran."""
        lang = language or self.__language
        return (
            MetaSurahs(self.path_database, lang)
            if lang
            else MetaSurahs(self.path_database)
        )

    def memory_quran(self) -> MemoryQuran:
        """Retourne l'outil de gestion des parties du Coran à mémoriser."""
        return MemoryQuran(self.path_database)

    def quran_reader(self) -> MetaQuranReader:
        """Retourne un lecteur du texte du Coran avec métadonnées."""
        return MetaQuranReader(self.path_database)

    def youtube_services(self) -> YoutubeServices:
        if self.__youtube_instance is None:
            self.__youtube_instance = YoutubeServices()
        return self.__youtube_instance

    def setup_all(self, eager: bool = False) -> dict:
        """
        Initialise les fichiers et données (cache, CSV, etc.).
        Si eager=True, YoutubeServices est instancié immédiatement.
        """
        setup_info = {
            "meta_surahs": self.meta_surahs(),
            "quran_reader": self.quran_reader(),
        }

        if eager:
            setup_info["youtube_services"] = self.youtube_services()

        return setup_info
