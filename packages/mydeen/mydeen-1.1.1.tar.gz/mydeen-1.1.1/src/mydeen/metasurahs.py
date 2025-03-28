import pandas as pd
import pathlib as plib
from .services import Services
from .quran_reader_base import QuranReaderBase as QuranReader
from .exception_error import ByError, FormatValueGet, SurahNotFound, VersetNotFound
from .interface import ListMetaSurahs
from typing import Tuple, Union, Optional, List, Any
from typing_extensions import Literal
import re

LanguageOptions = Literal['fr', 'en'] # francais ou anglais

class ParserMetaSurahs:
    def __init__(self, path_database: str, language:LanguageOptions) -> None:
        """
        Initialise la classe ParserMetaSurahs qui gère le parsing des métadonnées des sourates.

        Args:
            path_database (str): Le chemin vers la base de données.
        """
        self.path_database = path_database
        self.__services = Services()
        self.__response_api = self._request_response_api()
        self.__quran_reader = QuranReader(path_database)
        self.__language:LanguageOptions = self.normalize_language_code(language)

    @property
    def language(self):
        return self.__language

    def normalize_language_code(self, name: LanguageOptions) -> LanguageOptions:
        if name not in list(LanguageOptions.__args__):
            return 'en' # par default en
        return name

    def _request_response_api(self) -> dict:
        """
        Récupère les données de l'API des métadonnées des sourates.

        Returns:
            dict: La réponse de l'API sous forme de dictionnaire.
        """
        return self.__services.metadata_off_surahs()

    def parser_response_api(self) -> pd.DataFrame:
        """
        Parse les métadonnées des sourates provenant de l'API.

        Returns:
            pd.DataFrame: Un DataFrame contenant les métadonnées des sourates et les informations sur les sajdas.
        """
        responseapi = self.__response_api
        data_response = responseapi["data"]
        surahs = data_response["surahs"]["references"]
        sajdas = data_response["sajdas"]["references"]
        df_surahs = pd.DataFrame(surahs)
        df_sajdas = pd.DataFrame(sajdas)
        df_merged = pd.merge(
            df_surahs, df_sajdas, how="left", left_on=["number"], right_on=["surah"]
        )
        df_merged.drop(columns=["surah", "ayah"], inplace=True)
        df_merged["sajdas_recommended"] = (
            df_merged["recommended"]
            .apply(lambda x: False if pd.isna(x) else x)
            .astype(bool)
        )
        df_merged["sajdas_obligatory"] = (
            df_merged["obligatory"]
            .apply(lambda x: False if pd.isna(x) else x)
            .astype(bool)
        )
        df_merged.drop(columns=["recommended", "obligatory"], inplace=True)
        df_merged.drop_duplicates(inplace=True)
        return df_merged

    def parser_quran_reader(self) -> pd.DataFrame:
        """
        Parse les données des sourates du Coran (sans versets).

        Returns:
            pd.DataFrame: Un DataFrame contenant les informations des sourates (nom, traduction, type de révélation, etc.).
        """
        quran = self.__quran_reader.quran
        sourates_data = [
            {
                "position": sourate["position"],
                "name_arabic": sourate["nom"],
                "name_phonetic": sourate["nom_phonetique"],
                "name_english": sourate["englishNameTranslation"],
                "name_french": sourate["nom_sourate"],
                "revelation_type": sourate["revelation"],
            }
            for sourate in quran["sourates"]
        ]
        df = pd.DataFrame(sourates_data)
        df.drop_duplicates(inplace=True)
        return df

    def parser_meta_surahs(self, save_in: bool = True) -> pd.DataFrame:
        """
        Fusionne les données des sourates provenant de l'API et du fichier du Coran pour créer un DataFrame complet.

        Args:
            save_in (bool): Si True, sauvegarde le DataFrame résultant dans un fichier CSV.

        Returns:
            pd.DataFrame: Un DataFrame contenant toutes les métadonnées des sourates fusionnées.
        """
        parser_quran_reader = self.parser_quran_reader()
        parser_response_api = self.parser_response_api()

        merged_df = pd.merge(
            parser_response_api,
            parser_quran_reader,
            left_on="number",
            right_on="position",
            how="left",
        )

        merged_df = merged_df[
            [
                "number",
                "name_arabic",
                "name_phonetic",
                "name_english",
                "name_french",
                "revelation_type",
                "numberOfAyahs",
                "sajdas_recommended",
                "sajdas_obligatory",
            ]
        ]
        merged_df.rename(
            columns={
                "number": "position",
                "name_arabic": "name_arabic",
                "name_phonetic": "name_phonetic",
                "name_english": "name_english",
                "name_french": "name_french",
                "revelation_type": "revelation_type",
                "numberOfAyahs": "number_of_ayahs",
            },
            inplace=True,
        )
        merged_df["url_quran"] = merged_df["position"].apply(
            lambda x: self.define_url_quran_com(x)
        )
        merged_df.drop_duplicates(inplace=True)
        if save_in:
            path = plib.Path(self.path_database).joinpath(
                f"metasurahs_{self.language}.csv"
            )
            merged_df.to_csv(index=False, path_or_buf=path.as_posix())
        return merged_df

    def define_url_quran_com(self, surah: Any = None) -> str:
        base_url = "https://quran.com"
        if self.__language == "en":
            return f"{base_url}/{surah}" if surah else base_url
        return (
            f"{base_url}/{self.__language}/{surah}"
            if surah
            else f"{base_url}/{self.__language}"
        )


class MetaSurahs:
    def __init__(self, path_database: str, language: str = "fr") -> None:
        """
        Initialise la classe MetaSurahs en chargeant les données des sourates depuis un fichier CSV
        ou en les générant via le ParserMetaSurahs si le fichier n'existe pas.

        Args:
            path_database (str): Le chemin vers la base de données.
        """
        parser = ParserMetaSurahs(path_database, language)
        lang_code = parser.language
        path = plib.Path(path_database).joinpath(f"metasurahs_{lang_code}.csv")
        if path.exists():
            df = pd.read_csv(path.as_posix())
        else:
            df = parser.parser_meta_surahs()
        self.__df = df
        self.__language = lang_code

    @property
    def language(self) -> LanguageOptions:
        return self.__language

    @property
    def df(self) -> pd.DataFrame:
        """
        Retourne le DataFrame contenant les métadonnées des sourates.

        Returns:
            pd.DataFrame: Le DataFrame des sourates.
        """
        return self.__df

    @property
    def columns_names(self) -> List[str]:
        """
        Retourne la liste des noms de colonnes dans le DataFrame.

        Returns:
            List[str]: La liste des noms de colonnes.
        """
        return list(self.df.columns)

    def get_by(
        self, by: str, value: Union[Any, Tuple, List, None], respapi: bool = True
    ) -> Optional[Union[ListMetaSurahs, pd.DataFrame]]:
        """
        Récupère les enregistrements filtrés par une colonne spécifique et une valeur.
        Si value est None, retourne toutes les données de la colonne 'by'.
        Convertit les valeurs en chaînes de caractères pour éviter les erreurs de typage.

        Args:
            by (str): Le nom de la colonne sur laquelle filtrer.
            value (Union[Any, Tuple, List, None]): La valeur ou les valeurs à filtrer, ou None pour récupérer toutes les données de la colonne.
            respapi (bool): Si True, retourne un dictionnaire JSON.

        Returns:
            Optional[Union[ListMetaSurahs, pd.DataFrame]]: Les données filtrées ou None si aucune donnée.
        """
        if by not in self.columns_names:
            raise ByError(f"Column name invalid {by}")
        if value is None:
            data = self.df[[by]]
        elif isinstance(value, (tuple, list)):
            value = [str(v) for v in value]
            data = self.df[self.df[by].astype(str).isin(value)]
        else:
            value = str(value)  # Convertir la valeur en chaîne de caractères
            data = self.df[self.df[by].astype(str) == value]
        if data.empty:
            return None
        return data.to_dict(orient="records") if respapi else data

    def get_all(self, respapi: bool = True) -> Union[ListMetaSurahs, pd.DataFrame]:
        """
        Retourne toutes les données.

        Args:
            respapi (bool): Si True, retourne les données formatées pour une API (sous forme de liste de dictionnaires).
                            Si False, retourne les données sous forme brute (DataFrame).

        Returns:
            Union[List[dict], pd.DataFrame]: Toutes les données sous forme de dictionnaire (API) ou DataFrame (brut).
        """
        return self.df.to_dict(orient="records") if respapi else self.df

    def sort_by_ayahs(
        self, order: Literal["asc", "desc"], respapi: bool = True
    ) -> Union[ListMetaSurahs, pd.DataFrame]:
        """
        Trie les données par nombre de versets (ayahs).

        Args:
            order (Literal['asc', 'desc']): L'ordre de tri (ascendant ou descendant).
            respapi (bool): Si True, retourne un dictionnaire JSON.

        Returns:
            Union[ListMetaSurahs, pd.DataFrame]: Les données triées.
        """
        data = self.df.sort_values(
            by="number_of_ayahs", ascending=True if order == "asc" else False
        )
        return data.to_dict(orient="records") if respapi else data

    def check_format_get(self, value: str) -> bool:
        pattern = r"^\d+(?::\d+)?$"
        return bool(re.match(pattern, value))

    def _extract_get(self, value: str) -> Tuple[int, Optional[int]]:
        """
        Extrait les valeurs de la requête get.
        """
        if not self.check_format_get(value):
            raise FormatValueGet("Format value not matched")
        values = value.split(":")
        if len(values) > 1:
            surah, verset = values
            surah = int(surah)
            verset = int(verset)
            return surah, verset
        else:
            values = int(values[0])
            return values, None

    def get(self, value: str):
        """
        Récupère les données d'une sourate et d'un verset spécifiques.
        """
        surah, verset = self._extract_get(value)
        data_s = self.get_by("position", surah)
        if data_s is None:
            raise SurahNotFound("Surah not found")
        if verset is not None:
            if verset > data_s[0]["number_of_ayahs"]:
                raise VersetNotFound("Verset not found")
            for surah in data_s:
                new_url = surah["url_quran"] + f"?startingVerse={verset}"
                surah["url_quran"] = new_url
        return data_s

    def get_surahs(self, pos_a: int, pos_b: int) -> ListMetaSurahs:
        """
        Récupère les données des sourates entre deux positions.
        """
        data = self.df[(self.df["position"] >= pos_a) & (self.df["position"] <= pos_b)]
        return data.to_dict(orient="records")

    def get_by_nb_ayahs(self, nb_ayah: int) -> ListMetaSurahs:
        """
        Récupère les sourates ayant un nombre spécifique de versets (ayahs).

        Args:
            nb_ayah (int): Le nombre de versets (ayahs) à rechercher.

        Returns:
            ListMetaSurahs: Une liste de dictionnaires contenant les métadonnées des sourates correspondantes.
        """
        data = self.df[self.df["number_of_ayahs"] == nb_ayah]
        return data.to_dict(orient="records")
