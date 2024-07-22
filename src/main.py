import pandas as pd

from src.reports import reports
from src.services import operation_finder
from src.utils import xlsx_reader
from src.views import process_data


def main() -> None:
    """
    Основная функция, запускающая другие.
    """
    file_path = "../data/operations.xls"
    data = xlsx_reader(file_path)
    request = input("Введите категорию\n")

    process_data(data)
    operation_finder(data, request)
    reports(pd.read_excel(file_path))


if __name__ == "__main__":
    main()
