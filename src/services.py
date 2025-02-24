import json

import pandas as pd

from utils import get_formated_transactions, get_transactions_data


def simple_search(search_string: str) -> object:
    """
    Принимает строку для поиска.
    Возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или в категории.
    """

    transactions: pd.DataFrame = get_transactions_data()

    found_transactions = transactions.loc[
        (
            (transactions["Категория"].str.contains(search_string, case=False))
            | (transactions["Описание"].str.contains(search_string, case=False)) & (transactions["Статус"] == "OK")
        )
    ]
    formatted_transactions: list = get_formated_transactions(found_transactions)

    return json.dumps(formatted_transactions, ensure_ascii=False)


def mobile_transactions() -> object:
    """
    Функция возвращает JSON-файл со всеми транзакциями, содержащими в описании мобильные номера.
    """

    transactions: pd.DataFrame = get_transactions_data()

    found_transactions = transactions.loc[
        (
            (transactions["Описание"].str.contains(r"\+\d\s\d\d\d\s\d\d\d\-\d\d\-\d\d", case=False))
            & (transactions["Статус"] == "OK")
        )
    ]
    formatted_transactions: list = get_formated_transactions(found_transactions)

    return json.dumps(formatted_transactions, ensure_ascii=False)


def individual_transactions() -> object:
    """
    Функция возвращает JSON-файл со всеми транзакциями, которые относятся к переводам физическим лицам.
    Категория такой транзакции — Переводы, а в описании есть имя и первая буква фамилии с точкой.
    """

    transactions: pd.DataFrame = get_transactions_data()

    found_transactions = transactions.loc[
        (
            (transactions["Описание"].str.contains(r"\b\D\.", case=False))
            & (transactions["Статус"] == "OK")
            & (transactions["Категория"] == "Переводы")
        )
    ]
    formatted_transactions: list = get_formated_transactions(found_transactions)

    return json.dumps(formatted_transactions, ensure_ascii=False)
