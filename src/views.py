import datetime
import json

import pandas as pd

from external_api import get_currency_rates, get_stock_prices
from utils import get_transactions_data


def main_screen(date_string: str) -> object:
    """Принимает на вход дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС. Для работы с данными использует другие функции.
    Возвращает JSON-ответ со следующими данными:
    1. Приветствие в формате "???", где ??? — «Доброе утро» / «Добрый день» /
    «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
    2. По каждой карте:
    - последние 4 цифры карты;
    - общая сумма расходов;
    - кешбэк (1 рубль на каждые 100 рублей).
    3. Топ-5 транзакций по сумме платежа.
    4. Курс валют.
    5. Стоимость акций из S&P500.
    """

    # пробуем привести данные в нужный формат
    try:

        # получаем объект даты и времени
        date_object: datetime.datetime = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        greeting = ""

        # проверяем время дня для определения приветствия
        if 0 <= date_object.hour < 5:
            greeting = "Доброй ночи"

        elif 5 <= date_object.hour < 12:
            greeting = "Доброе утро"

        elif 12 <= date_object.hour < 18:
            greeting = "Добрый день"

        else:
            greeting = "Добрый вечер"

    except ValueError:
        # если формат не соответствует необходимому, завершаем работу
        return []

    except TypeError:
        # если тип данных не соответствует необходимому, завершаем работу
        return None

    # если данные корректные, продолжаем работу
    else:

        transactions: pd.DataFrame = get_transactions_data()

        # фильтруем по дате, с 1 числа месяца до указанной даты
        filtered_by_date = transactions[
            (transactions["Дата операции"] >= date_object.replace(day=1, hour=0, minute=0, second=0))
            & (transactions["Дата операции"] <= date_object)
        ]

        # отбираем все успешные операции с тратами
        needed_data = filtered_by_date[(filtered_by_date["Сумма операции"] < 0) & (filtered_by_date["Статус"] == "OK")]

        # группируем по номеру карты и формируем в словарь
        grouped_transactions = needed_data.groupby("Номер карты").agg({"Сумма операции": "sum"})
        card_information: dict = grouped_transactions.to_dict()

        full_information: list = []

        # проходимся по словарю и отбираем нужную информацию, складываю ее в список словарей
        for key, value in card_information["Сумма операции"].items():
            positive_total: str = str(value).replace("-", "")
            data_dict: dict = {
                "last_digits": key,
                "total_spent": positive_total,
                "cashback": float(positive_total) // 100,
            }
            full_information.append(data_dict)

        top_transactions: list = []

        # сортируем все транзакции по сумме операции
        sorted_by_amount = needed_data.sort_values("Сумма операции", ascending=True)

        # проходимся по каждой транзакцией и записываем нужные данные в словарь
        for _, row in sorted_by_amount.iterrows():
            positive_amount: str = str(row["Сумма операции"]).replace("-", "")
            chosen_transaction: dict = {
                "date": row["Дата платежа"],
                "amount": positive_amount,
                "category": row["Категория"],
                "description": row["Описание"],
            }
            top_transactions.append(chosen_transaction)
            if len(top_transactions) == 5:  # проверяем, есть ли уже 5 операций в списке
                break

        # собираем все данные вместе и превращаем в JSON-файл
        result: dict = {
            "greeting": greeting,
            "cards": full_information,
            "top_transactions": top_transactions,
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices(),
        }

        return json.dumps(result, ensure_ascii=False)
