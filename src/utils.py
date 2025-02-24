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
        # при возникновении ошибки, возвращаем пустой словарь.
        return {}

    else:
        return converted_data


def get_transactions_data(path_file: str = "data/operations.xlsx") -> pd.DataFrame:
    """
    Принимает путь до XLSX-файла с транзакциями и возвращает список словарей с данными.
    Если файл пустой или не найден, возвращает пустой список.
    """

    try:
        # пробуем прочитать файл
        dataframe = pd.read_excel(os.path.join(PATH_HOME, path_file))

        dataframe["Дата операции"] = pd.to_datetime(dataframe["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        return dataframe

    except Exception:
        # при возникновении ошибки, возвращаем пустой список.
        raise


def get_formated_transactions(transactions: pd.DataFrame) -> list:
    """
    Форматирует полученные транзакции в формате pd.DataFrame по шаблону в объект Python - словарь.
    Возвращает список словарей со всеми транзакциями.
    """

    formatted_transactions: list = []

    for _, row in transactions.iterrows():
        positive_amount: str = str(row["Сумма операции"]).replace("-", " ")
        transaction_data: dict = {
            "date": row["Дата платежа"],
            "last_digits": row["Номер карты"],
            "amount": positive_amount,
            "currency": row["Валюта платежа"],
            "category": row["Категория"],
            "description": row["Описание"],
        }
        formatted_transactions.append(transaction_data)

    return formatted_transactions
