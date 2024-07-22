import json
import re

from src.logger import logging_setup

logger = logging_setup()


def operation_finder(data: list[dict], user_request: str) -> str:
    """
    Функция принимает список с транзакциями и запрос от пользователя.
    Возвращает список транзакций имеющих в описании запрос от пользователя.
    """
    final_data = []
    for operation in data:
        if re.search(user_request, str(operation["Описание"])):
            final_data.append(operation)
    logger.info("Сработала operation_finder.")
    return json.dumps(final_data, indent=4, ensure_ascii=False)
