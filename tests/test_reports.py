import pandas as pd

from src import reports


def test_spending_by_category():
    test_data = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                ["27.12.2021 12:00:00", "28.12.2021 13:00:00", "15.11.2021 10:00:00"], format="%d.%m.%Y %H:%M:%S"
            ),
            "Категория": ["Каршеринг", "Такси", "Каршеринг"],
            "Сумма операции": [-100, -200, -150],
        }
    )

    result = reports.spending_by_category("Каршеринг", transactions=test_data, date="27.12.2021")

    assert len(result) == 1
    assert "Дата операции" in result.columns
    assert "Сумма операции" in result.columns
    assert result.iloc[0]["Сумма операции"] == -100


def test_spending_by_category_no_date():
    import datetime

    now = datetime.datetime.now()

    test_data = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [f"01.{now.month}.{now.year} 12:00:00", f"15.{now.month}.{now.year} 13:00:00"],
                format="%d.%m.%Y %H:%M:%S",
            ),
            "Категория": ["Каршеринг", "Такси"],
            "Сумма операции": [-100, -200],
        }
    )

    result = reports.spending_by_category("Каршеринг", transactions=test_data, date=None)
    assert isinstance(result, pd.DataFrame)


def test_record_to_file():
    test_data = [{"test": "data"}]

    @reports.record_to_file("test.json")
    def sample_function():
        return test_data

    result = sample_function()
    assert result == test_data
