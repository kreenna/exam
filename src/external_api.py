import os

import requests
from dotenv import load_dotenv

from utils import get_user_settings


def get_currency_rates(user_settings_data: str = "user_settings.json") -> list:
    """
    Принимает на вход опциональный путь до JSON-файла с настройками пользователя.
    Возвращает список словарей со стоимостью каждой из валют из настроек.
    """

    # получаем валюты из настроек юзера
    user_currencies: list = get_user_settings(user_settings_data)["user_currencies"]

    currency_rates: list = []

    for currency in user_currencies:

        # подгружаем API_KEY
        load_dotenv()
        API_KEY = os.getenv("CURRENCY_API_KEY")  # получаем API-ключ

        url: str = "https://api.apilayer.com/exchangerates_data/convert"
        payload: dict = {"to": "RUB", "from": currency, "amount": "1", "apikey": API_KEY}  # задаем параметры

        response = requests.get(url, params=payload)  # получаем ответ
        currency_rate: float = response.json()["info"]["rate"]

        # создаем словарь для каждой валюты
        currency_info: dict = {"currency": currency, "rate": currency_rate}

        # добавляем словарь в список валют
        currency_rates.append(currency_info)

    return currency_rates


def get_stock_prices(user_settings_data: str = "user_settings.json") -> list:
    """
    Принимает на вход опциональный путь до JSON-файла с настройками пользователя.
    Возвращает список словарей со стоимостью каждой из акций из настроек.
    """

    # получаем валюты из настроек юзера
    user_stocks: list = get_user_settings(user_settings_data)["user_stocks"]

    stock_prices: list = []

    for stock in user_stocks:

        # подгружаем API_KEY
        load_dotenv()
        API_KEY = os.getenv("STOCKS_API_KEY")  # получаем API-ключ

        url: str = "https://www.alphavantage.co/query"
        payload: dict = {"function": "GLOBAL_QUOTE", "symbol": stock, "apikey": API_KEY}  # задаем параметры

        response = requests.get(url, params=payload)  # получаем ответ
        stock_price: float = response.json()["Global Quote"]["05. price"]

        # создаем словарь для каждой валюты
        currency_info: dict = {"stock": stock, "rate": stock_price}

        # добавляем словарь в список валют
        stock_prices.append(currency_info)

    return stock_prices
