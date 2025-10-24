from unittest.mock import patch

import pandas as pd
import pytest

from src import views


def test_time_greetings():
    assert views.time_greetings("25-11-2003 05:00:00") == "Доброй ночи"
    assert views.time_greetings("25-11-2003 08:00:00") == "Доброе утро"
    assert views.time_greetings("25-11-2003 14:00:00") == "Добрый день"
    assert views.time_greetings("25-11-2003 20:00:00") == "Добрый вечер"


@patch("pandas.read_excel")
def test_load_data(mock_read_excel):
    test_data = pd.DataFrame({"test": [1, 2, 3]})
    mock_read_excel.return_value = test_data

    result = views.load_data("fake_path.xlsx")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


def test_get_card_data():
    test_data = pd.DataFrame({"Номер карты": ["1234567812345678", "8765432187654321"], "Сумма операции": [-100, -200]})

    result = views.get_card_data(test_data)

    assert len(result) == 2
    assert result[0]["last_digits"] == "5678"


def test_get_card_data_no_card_column():
    test_data = pd.DataFrame({"Другой столбец": [1, 2, 3], "Сумма операции": [100, 200, 300]})

    with pytest.raises(Exception, match="Данные недействительны"):
        views.get_card_data(test_data)


def test_get_top_transactions():
    test_data = pd.DataFrame(
        {
            "Дата операции": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "Сумма операции": [5000, 1000, 3000],
            "Категория": ["Еда", "Транспорт", "Развлечения"],
            "Описание": ["Ресторан", "Такси", "Кино"],
        }
    )

    result = views.get_top_transactions(test_data)

    assert len(result) == 3
    assert result[0]["amount"] == 5000


@patch("requests.request")
@patch("os.getenv")
def test_get_currency_rates(mock_getenv, mock_request):
    mock_getenv.return_value = "fake_key"
    mock_request.return_value.text = '{"result": 75.5}'

    result = views.get_currency_rates()

    assert len(result) == 2
    first_item = result[0]
    assert first_item["currency"] == "USD"


@patch("requests.request")
@patch("os.getenv")
def test_get_currency_rates_error(mock_getenv, mock_request):
    mock_getenv.return_value = "fake_key"
    mock_request.side_effect = Exception("API error")

    result = views.get_currency_rates()
    assert "Ошибка" in result


@patch("requests.get")
@patch("os.getenv")
def test_get_stock_prices(mock_getenv, mock_get):
    mock_getenv.return_value = "fake_key"
    mock_get.return_value.json.return_value = {"data": [{"close": 150}]}

    result = views.get_stock_prices()

    assert len(result) == 5
    first_item = result[0]
    assert first_item["stock"] == "AAPL"


@patch("requests.get")
@patch("os.getenv")
def test_get_stock_prices_error(mock_getenv, mock_get):
    mock_getenv.return_value = "fake_key"
    mock_get.side_effect = Exception("API error")

    result = views.get_stock_prices()
    assert "Ошибка" in result
