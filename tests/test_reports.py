from typing import Any, Optional
from unittest import TestCase, mock

import pandas as pd

from src.reports import spending_by_category

data = [
    {
        "Дата операции": "31.12.2021 01:23:42",
        "Дата платежа": "31.12.2021",
        "Номер карты": "*5091",
        "Статус": "OK",
        "Сумма операции": -564.00,
        "Валюта операции": "RUB",
        "Сумма платежа": -564.00,
        "Валюта платежа": "RUB",
        "Категория": "Различные товары",
        "MCC": "5399",
        "Описание": "Ozon.ru",
        "Бонусы (включая кэшбэк)": 5.00,
        "Округление на инвесткопилку": 0.00,
        "Сумма операции с округлением": 564.00,
    },
    {
        "Дата операции": "31.10.2018 20:31:00",
        "Дата платежа": "31.10.2018",
        "Номер карты": "*7081",
        "Статус": "OK",
        "Сумма операции": -2018.00,
        "Валюта операции": "RUB",
        "Сумма платежа": -2018.00,
        "Валюта платежа": "RUB",
        "Категория": "Супермаркеты",
        "MCC": "5399",
        "Описание": "Колхоз",
        "Бонусы (включая кэшбэк)": 5.00,
        "Округление на инвесткопилку": 0.00,
        "Сумма операции с округлением": -2013.00,
    },
]
df = pd.DataFrame(data)


class TestSpendingByCategory(TestCase):
    def setUp(self) -> None:
        self.data: pd.DataFrame = pd.DataFrame(data)

    @mock.patch("src.reports.logger")
    def test_spending_by_category_exists(self, mock_logger: Any) -> None:
        result: Optional[pd.DataFrame] = spending_by_category(self.data, "Различные товары")
        self.assertIsNotNone(result)
        if result:
            self.assertEqual(len(result), 0)
        mock_logger.info.assert_called_once()
        mock_logger.error.assert_not_called()

    @mock.patch("src.reports.logger")
    def test_spending_by_category_not_exists(self, mock_logger: Any) -> None:
        result: Optional[pd.DataFrame] = spending_by_category(self.data, "Одежда")
        self.assertIsNone(result)
        mock_logger.error.assert_called_once()
        mock_logger.info.assert_not_called()
