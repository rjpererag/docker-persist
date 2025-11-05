import pandas as pd
from datetime import datetime
from tqdm import tqdm

from .data_fetcher import Fetcher
from ..utils import logger, FileManager


class FakeAPI:

    def __init__(self):
        self.now_str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.api = Fetcher()
        self.file_manager = FileManager()
        self.filesystem = self.file_manager.build_filesystem()

        self.cache = self._create_cache()

    @staticmethod
    def _create_cache() -> dict:
        return {
            "raw": [],
            "formatted": {
                "json": [],
                "csv": pd.DataFrame(),
            }
        }

    @staticmethod
    def _format_data(data: dict) -> dict:
        return {
            "city_name": data.get('data', {}).get('name'),
            "country_name": data.get('data', {}).get('stats', {}).get('country'),
            "population": data.get('data', {}).get('stats', {}).get('population'),
            "timestamp": data.get('timestamp')
        }

    def fetch(self) -> dict:
        response = self.api.fetch_fake_data()
        json_data = self._format_data(data=response)

        self.cache["raw"].append(response)
        self.cache["formatted"]["json"].append(json_data)
        self.file_manager.save_json(
            path=f'{self.filesystem["json"]}/{self.now_str}',
            data=self.cache["formatted"]["json"],
        )
        return json_data


    def _build_csv(self) -> pd.DataFrame:
        if len(self.cache["formatted"]["json"]) > 0:
            df = pd.DataFrame(self.cache["formatted"]["json"])
            self.file_manager.save_csv(
                path = f'{self.filesystem["csv"]}/{self.now_str}',
                data=df,
            )
            self.file_manager.save_xlsx(
                path = f'{self.filesystem["xlsx"]}/{self.now_str}',
                data=df,
            )
            return df
        return pd.DataFrame()

    def _collect(self, size: int):

            for i in tqdm(
                    iterable=range(size),
                    total=size,
                    desc="Collecting data",
            ):
                try:
                    self.fetch()
                except Exception as e:
                    logger.error(f"Error collecting data. id = {i}. {str(e)}")

    def fetch_multiple(
            self,
            size: int = 10,
            format_: str = 'json'
    ) -> list[dict] | pd.DataFrame:

        self._collect(size=size)
        self.cache["formatted"]["csv"] = self._build_csv()

        if format_ == 'csv':
            return self.cache["formatted"]["csv"]

        return self.cache["formatted"]["json"]
