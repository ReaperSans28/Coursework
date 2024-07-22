import json
from datetime import datetime as dt
from typing import Any, Optional

import pandas as pd

from src.logger import logging_setup

logger = logging_setup()


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[Any] = None
) -> Optional[pd.DataFrame]:
    """
    Функция возвращает траты за 3 месяца до введенной даты (Если дата не указана, по умлочанию стоит сегодняшняя).
    """
    if category not in transactions["Категория"].values:
        logger.error("Category is None.")
        return None

    transactions_data = transactions[transactions["Категория"].str.contains(category, case=False, na=False)]
    transactions_data.loc[:, "Дата платежа"] = pd.to_datetime(transactions_data["Дата платежа"], dayfirst=True)

    if date is None:
        date = dt.now().strftime("%d.%m.%Y")

    start_date = pd.to_datetime(date, format="%d.%m.%Y") - pd.DateOffset(months=3)

    filtered_data = transactions_data[transactions_data["Дата платежа"].notnull()]
    filtered_data = filtered_data[
        filtered_data["Дата платежа"].between(start_date, pd.to_datetime(date, format="%d.%m.%Y"))
    ]

    logger.info(filtered_data)

    if filtered_data is None:
        logger.error("filtered_data is None.")
        return None

    return filtered_data


def reports(data: pd.DataFrame) -> Optional[str]:
    """
    Вызов функции spending_by_category.
    """
    try:
        category = input("По какой категории нужно произвести поиск?\n")
        date = input("Какая дата окончания? (день.месяц.год)\n")
        return json.dumps(spending_by_category(data, category, date), indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
