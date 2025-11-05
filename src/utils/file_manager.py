import os
import pandas as pd
import pickle
import json

from .logger import logger


class FileManager:
    """
    File manager that provides methods to save data in json, csv, xlsx and pkl formats.
    Includes logic to set up a directory tree which holds dedicated directories for
    each of the mentioned extensions. Example (results/json or results/csv))
    """

    @staticmethod
    def _review_extension(path: str, extension: str) -> str:
        if extension not in path:
            return f"{path}.{extension}"
        return path

    def save_json(self, path: str, data: list | dict, indent: int = 2) -> None:
        try:
            path = self._review_extension(path=path, extension="json")
            logger.info("Saving json file at %s", path)
            if (not isinstance(data, list)) or (not isinstance(data, dict)):
                logger.error(f"Data is not a list or dict: {type(data)}")
                return

            with open(path, "w") as json_file:
                json.dump(data, json_file, indent=indent)
        except Exception as e:
            logger.error(f"Failed saving {path}: {str(e)}")


    def save_csv(self, path: str, data: pd.DataFrame, index: bool = False) -> None:
        try:
            path = self._review_extension(path=path, extension="csv")
            logger.info("Saving csv file at %s", path)
            if not isinstance(data, pd.DataFrame):
                logger.error(f"Data is not a valid DataFrame: {type(data)}")
                return

            data.to_csv(path, index=index)
        except Exception as e:
            logger.error(f"Failed saving {path}: {str(e)}")


    def save_xlsx(self, path: str, data: pd.DataFrame, index: bool = False) -> None:
        try:
            path = self._review_extension(path=path, extension="xlsx")
            logger.info("Saving xlsx file at %s", path)
            if not isinstance(data, pd.DataFrame):
                logger.error(f"Data is not a valid DataFrame: {type(data)}")
                return

            data.to_csv(path, index=index)
        except Exception as e:
            logger.error(f"Failed saving {path}: {str(e)}")

    def save_pkl(self, path: str, data) -> None:
        try:
            path = self._review_extension(path=path, extension="pkl")
            logger.info("Saving pkl file at %s", path)
            with open(path, "wb") as pickle_file:
                pickle.dump(data, pickle_file)
        except Exception as e:
            logger.error(f"Errr saving pickle path: {path}. {str(e)}")

    def build_filesystem(self, root_dir: str = "results") -> dict:
        logger.info("Building filesystem")
        dir_tree = self._get_dir_tree(root_dir = root_dir)
        for dir_ in dir_tree.values():
            self._validate_dir(dir_path=dir_)

        return dir_tree

    @staticmethod
    def _validate_dir(dir_path: str) -> None:
        if not os.path.exists(dir_path):
            logger.info(f"Creating {dir_path}")
            os.mkdir(dir_path)
        else:
            logger.info(f"Skipping {dir_path} already exists")

    @staticmethod
    def _get_dir_tree(root_dir: str) -> dict:
        extensions = ["json", "csv", "xlsx", "pkl"]
        dirs = {"root_dir": root_dir}

        for ext in extensions:
            dirs[ext] = f"{root_dir}/{ext}"

        return dirs






