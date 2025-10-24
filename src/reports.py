import datetime
import json
import os.path
from typing import Any, Optional

import pandas as pd

from src.views import load_data


def spending_by_category(
    category: str, transactions: pd.DataFrame = load_data(), date: Optional[str] = datetime.datetime.now()
) -> pd.DataFrame:
    """возвращает траты по заданной категории за последние три месяца"""
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    if date:
        target_date = datetime.datetime.strptime(date, "%d.%m.%Y")
        target_month = target_date.month
        target_year = target_date.year
    else:
        target_month = datetime.datetime.now().month
        target_year = datetime.datetime.now().year

    result = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"].dt.month == target_month)
        & (transactions["Дата операции"].dt.year == target_year)
    ]

    return result


def record_to_file(filename: str = "имя файла") -> str | Any:
    """записывает в файл результат, который возвращает функция, формирующая отчет"""
    filename = os.path.join(os.path.dirname(__file__), "..", "data", filename)

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, "w", newline="", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Сохранено в {filename}")
            return result

        return wrapper

    return decorator


print(spending_by_category("Каршеринг", date="27.12.2021"))
