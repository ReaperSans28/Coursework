from unittest import TestCase, mock
from unittest.mock import MagicMock

from src.views import (get_currency_rates, get_stock_prices, hello, process_cards_data, top_five_transactions)

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


def test_hello() -> None:
    assert isinstance(hello(), str)


def test_get_currency_rates() -> None:
    assert type(get_currency_rates()) is dict
    assert len(get_currency_rates()) == 2
    assert "USD" in get_currency_rates()
    assert "EUR" in get_currency_rates()


class TestGetStockPrices(TestCase):

    @mock.patch("requests.get")
    def test_get_stock_prices_success(self, mock_get: MagicMock) -> None:
        mock_json_data = {"Global Quote": {"02. open": "1500.0"}}
        mock_get.return_value.json.return_value = mock_json_data
        result = get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        for stock_data in result:
            self.assertIsInstance(stock_data, dict)
            self.assertIn("stock", stock_data)
            self.assertIn("rate", stock_data)
            self.assertIsInstance(stock_data["stock"], str)
            self.assertIsInstance(stock_data["rate"], float)

    @mock.patch("requests.get")
    def test_get_stock_prices_error(self, mock_get: MagicMock) -> None:
        mock_get.side_effect = Exception
        result = get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
        self.assertEqual(result, [])


def test_process_cards_data():
    data = [
        {
            "Номер карты": "1234567890123456",
            "Сумма операции": 100.0,
        },
        {
            "Номер карты": "abc123",
            "Сумма операции": 200.0,
        },
        {
            "Номер карты": "9876543210987654",
            "Сумма операции": 300.0,
        },
    ]
    result = process_cards_data(data)
    assert len(result) == 3
    assert result[0]["last_digits"] == "3456"
    assert result[0]["total_spent"] == 100.0
    assert result[0]["cashback"] == 1.0
    assert result[1]["last_digits"] == "c123"
    assert result[1]["total_spent"] == 200.0
    assert result[1]["cashback"] == 2.0


def test_process_cards_data_without_data():
    data = []
    result = process_cards_data(data)
    assert len(result) == 0


test_data = [
    {"Дата операции": "2023-10-27", "Сумма платежа": 1000, "Категория": "Продукты", "Описание": "Покупка в магазине"},
    {"Дата операции": "2023-10-26", "Сумма платежа": 500, "Категория": "Транспорт", "Описание": "Проезд на автобусе"},
    {"Дата операции": "2023-10-25", "Сумма платежа": 2000, "Категория": "Развлечения", "Описание": "Билеты в кино"},
    {"Дата операции": "2023-10-24", "Сумма платежа": 1500, "Категория": "Одежда", "Описание": "Покупка новой куртки"},
    {"Дата операции": "2023-10-23", "Сумма платежа": 300, "Категория": "Продукты", "Описание": "Покупка в супермаркете"},
    {"Дата операции": "2023-10-22", "Сумма платежа": 5000, "Категория": "Путешествия", "Описание": "Авиабилеты"},
]
expected_result = [
    {"date": "2023-10-22", "amount": 5000, "category": "Путешествия", "description": "Авиабилеты"},
    {"date": "2023-10-25", "amount": 2000, "category": "Развлечения", "description": "Билеты в кино"},
    {"date": "2023-10-24", "amount": 1500, "category": "Одежда", "description": "Покупка новой куртки"},
    {"date": "2023-10-27", "amount": 1000, "category": "Продукты", "description": "Покупка в магазине"},
    {"date": "2023-10-26", "amount": 500, "category": "Транспорт", "description": "Проезд на автобусе"},
]


def test_top_five_transactions():
    result = top_five_transactions(test_data)
    assert result == expected_result
