# test_services.py
import pandas as pd

from src import services


def test_simple_search():
    test_data = pd.DataFrame(
        {
            "Категория": ["Супермаркет", "Аптека", "Ресторан"],
            "Описание": ["Покупка в Пятерочке", "Таблетки", "Ужин в кафе"],
        }
    )

    services.df = test_data

    result = services.simple_search("аптека")
    assert len(result) == 1
    assert result[0]["Категория"] == "Аптека"
