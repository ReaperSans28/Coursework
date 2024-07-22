import pandas as pd

from src.logger import logging_setup

logger = logging_setup()


def xlsx_reader(file_path: str) -> list:
    """
    Функция для получения данных из xls файла.
    """
    try:
        data = pd.read_excel(file_path)
        data["Номер карты"] = data["Номер карты"].astype(str)
        return data.to_dict("records")
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        return []
