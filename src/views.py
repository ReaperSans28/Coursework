import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from src.logger import logging_setup

logger = logging_setup()

load_dotenv()

api_key1 = os.getenv("API_KEY")
api_key2 = os.getenv("POLYGON_API_KEY")
STOCK_API_URL = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?tickers=AAPL,AMZN,GOOGL,MSFT,TSLA&apiKey={api_key2}"


def hello() -> str:
    """
    Функция приветствия в зависимости от времени.
    """
    time_now = datetime.now().strftime("%H")
    if 4 < int(time_now) < 12:
        return "Доброе утро!"
    elif 12 <= int(time_now) < 18:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


def get_currency_rates() -> dict:
    """
    Выдает актуальный курс доллара и евро.
    """
    global api_key1

    rates = {}

    url = "https://open.er-api.com/v6/latest/USD"
    headers = {"apikey": api_key1}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200 and "rates" in data:
        if "USD" in data["rates"]:
            usd_rate = data["rates"]["RUB"]
            rates["USD"] = round(float(usd_rate), 2)
            logger.info("Сработала get_usd_value")

    url = "https://open.er-api.com/v6/latest/EUR"
    headers = {"apikey": api_key1}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200 and "rates" in data:
        if "EUR" in data["rates"]:
            euro_rate = data["rates"]["RUB"]
            rates["EUR"] = round(float(euro_rate), 2)
            logger.info("Сработала get_euro_value")

    if not rates:
        logger.error("get_exchange_rates не сработала, rates отсутствует")
        return {}

    return rates


def get_stock_prices(stocks: list) -> list:
    """
    Функция принимает лист с названиями акций и возвращает стоимость акций.
    """
    try:
        rates = []
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key2}"
            response = requests.get(url, timeout=30)
            data = round(float(response.json()["Global Quote"]["02. open"]), 2)
            rates.append({"stock": stock, "rate": data})
        logger.info(f"Сработала get_stock_prices")
        return rates
    except Exception as e:
        logger.error(f"Ошибка при получении цен акций: {e}")
        return []


def process_cards_data(data: list) -> list[dict]:
    """
    Функция принимает лист с транзакциями и возвращает лист с номером карты и суммами операций и кэшбэка.
    """
    cards_data: list[dict] = []
    for row in data:
        card_number = row["Номер карты"]
        last_digits = card_number[-4:]
        if last_digits != "nan":
            card_exists = False
            for card in cards_data:
                if card["last_digits"] == last_digits:
                    card["total_spent"] = round(row["Сумма операции"] + card["total_spent"], 2)
                    card["cashback"] = round((row["Сумма операции"] / 100) + card["cashback"], 2)
                    card_exists = True
                    break
            if not card_exists:
                cards_data.append(
                    {
                        "last_digits": last_digits,
                        "total_spent": row["Сумма операции"],
                        "cashback": round(row["Сумма операции"] / 100, 2),
                    }
                )
    logger.info("Сработала process_cards_data")
    return cards_data


def top_five_transactions(data: list) -> list:
    """
    Функция принимает лист с транзакциями и возвращает лист из 5 самых крупных.
    """
    top_transactions = sorted(data, key=lambda x: x["Сумма платежа"], reverse=True)[:5]
    top_transactions_data = [
        {
            "date": row["Дата операции"],
            "amount": row["Сумма платежа"],
            "category": row["Категория"],
            "description": row["Описание"],
        }
        for row in top_transactions
    ]
    logger.info("Сработала top_five_transactions")
    return top_transactions_data


def process_data(data: list) -> str:
    """
    Основная функция views.py запускающая остальные.
    """
    greeting = hello()
    cards_data = process_cards_data(data)
    top_transactions_data = top_five_transactions(data)
    currency_rates_data = get_currency_rates()
    stock_prices_data = get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])

    response = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions_data,
        "currency_rates": currency_rates_data,
        "stock_prices": stock_prices_data,
    }

    logger.info("Сработала process_data")
    return json.dumps(response, indent=4, ensure_ascii=False)
