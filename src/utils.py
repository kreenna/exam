import json
import os

import pandas as pd

from config import PATH_HOME


def get_user_settings(path_file: str) -> dict:
    """
    Принимает путь до JSON-файла с настройками и возвращает словарь с данными.
    Если файл пустой или не найден, возвращает пустой словарь.
    """

    # пробуем открыть файл
    try:
        with open(os.path.join(PATH_HOME, path_file), "r", encoding="utf-8") as file:
            converted_data: dict = json.load(file)

    except Exception:  # любые ошибки с файлом

        return {}

    else:
        return converted_data


def get_transactions_data(path_file: str) -> list:
    """
    Принимает путь до XLSX-файла с транзакциями и возвращает список словарей с данными.
    Если файл пустой или не найден, возвращает пустой список.
    """

    try:
        # пробуем прочитать файл
        df = pd.read_excel(os.path.join(PATH_HOME, path_file))

        # создаем список
        result: list = []

        # проходимся по каждой строке
        for _, row in df.iterrows():
            # заполняем словарь данными
            row_dict: dict = {
                "operation_date": (
                    row["Дата операции"].isoformat()
                    if isinstance(row["Дата операции"], pd.Timestamp)
                    else str(row["Дата операции"])
                ),
                "payment_date": (
                    row["Дата платежа"].isoformat()
                    if isinstance(row["Дата платежа"], pd.Timestamp)
                    else str(row["Дата платежа"])
                ),
                "card_number": row["Номер карты"] if pd.notna(row["Номер карты"]) else None,
                "state": row["Статус"],
                "operation_amount": row["Сумма операции"],
                "operation_currency": row["Валюта операции"],
                "payment_amount": row["Сумма платежа"],
                "payment_currency": row["Валюта платежа"],
                "cashback": row["Кэшбэк"] if pd.notna(row["Кэшбэк"]) else None,
                "category": row["Категория"],
                "MCC": row["MCC"] if pd.notna(row["MCC"]) else None,
                "description": row["Описание"],
                "bonuses": row["Бонусы (включая кэшбэк)"],
                "round_up": row["Округление на инвесткопилку"],
                "total_amount": row["Сумма операции с округлением"],
            }

            # добавляем словари в список
            result.append(row_dict)

        return result

    except Exception:
        # при возникновении ошибки, возвращаем пустой список.
        return []
