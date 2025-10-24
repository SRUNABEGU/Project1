import datetime
import json
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import unique
from pandas.core.interchange.dataframe_protocol import DataFrame

ABSPATH_TO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
load_dotenv()
RESULT = []


def time_greetings(date: str = "25-11-2003 06:00:01") -> str:
    """Возвращает приветствие в зависимости от времени суток"""

    date_obj = datetime.datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
    hour = date_obj.hour

    if 0 <= hour < 6:
        return "Доброй ночи"
    elif 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def load_data(path: str = ABSPATH_TO_FILE) -> DataFrame:
    """Загружает данные из Excel-файла и возвращает объект DataFrame"""

    df = pd.read_excel(path)
    return df


def get_card_data(df: pd.DataFrame = load_data()) -> list:
    """Обрабатывает DataFrame объект и возвращает данные по картам в виде JSON ответа"""

    card_numbers = []
    formatted_numbers = []
    card_data = []

    if "Номер карты" in df:

        for card in unique(df["Номер карты"]):
            if isinstance(card, str):
                card_numbers.append(card[-4:])
                formatted_numbers.append(df[df["Номер карты"] == card])

        for index, value in enumerate(formatted_numbers):
            card_data.append(
                {
                    "last_digits": card_numbers[index],
                    "total_spent": sum(value[value["Сумма операции"] < 0]["Сумма операции"]) * -1,
                    "cashback": (sum(value[value["Сумма операции"] < 0]["Сумма операции"]) * -1) / 100,
                }
            )

        return card_data
    else:
        raise Exception("Данные недействительны")


def get_top_transactions(df: pd.DataFrame = load_data()) -> list:
    """возващает список с 5 транзакциями с самой большой суммой платежа"""
    transactions_dict = df.to_dict("records")
    top_transactions = []

    transactions_dict.sort(key=lambda x: abs(x["Сумма операции"]), reverse=True)

    for i in range(5):
        if i < len(transactions_dict):
            item = transactions_dict[i]
            top_transactions.append(
                {
                    "date": item["Дата операции"],
                    "amount": abs(item["Сумма операции"]),
                    "category": item.get("Категория"),
                    "description": item.get("Описание"),
                }
            )
    return top_transactions


def get_currency_rates() -> str | list[Any]:
    """Возвращает ценнность валюты"""
    currency_rates = []

    try:
        for currency in ["USD", "EUR"]:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&" f"from={currency}&amount=1"
            payload = {}
            headers = {"apikey": f"{os.getenv('EXCHANGERATES_API_KEY')}"}
            response = requests.request("GET", url, headers=headers, data=payload)

            currency_rates.append({"currency": currency, "rate": round(json.loads(response.text)["result"], 2)})

        return currency_rates
    except Exception as error:
        return f"Ошибка: {error}"


def get_stock_prices() -> str | list[Any]:
    """возвращает список со стоимостью акций из S&P500"""
    stock_prices = []
    try:
        for index, stock in enumerate(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]):
            url = f"https://api.marketstack.com/v1/eod/latest?access_key={os.getenv('MARKETSTACK_API_KEY')}"
            querystring = {"symbols": stock}
            data = (requests.get(url, params=querystring)).json()

            stock_prices.append({"stock": stock, "price": data["data"][0]["close"]})

        return stock_prices
    except Exception as error:
        return f"Ошибка: {error}"


def main():
    """Основная функция"""
    RESULT.append(
        {
            "greetings": time_greetings(),
            "cards": get_card_data(),
            "top_transactions": get_top_transactions(),
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices(),
        }
    )
    print(json.dumps(RESULT, indent=2, ensure_ascii=False))
