from unittest.mock import patch

from src import main


@patch("main.time_greetings")
@patch("main.get_card_data")
@patch("main.get_top_transactions")
@patch("main.get_currency_rates")
@patch("main.get_stock_prices")
@patch("main.simple_search")
@patch("main.spending_by_category")
def test_main(mock_spending, mock_search, mock_stocks, mock_currency, mock_transactions, mock_cards, mock_greetings):
    # Настраиваем моки
    mock_greetings.return_value = "Добрый день"
    mock_cards.return_value = [{"test": "card"}]
    mock_transactions.return_value = [{"test": "transaction"}]
    mock_currency.return_value = [{"currency": "USD", "rate": 75.5}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150}]
    mock_search.return_value = [{"description": "test"}]
    mock_spending.return_value = "test spending report"

    # Очищаем RESULT и запускаем main
    main.RESULT = []
    main.main()

    # Проверяем что RESULT заполнился
    assert len(main.RESULT) == 1
    assert main.RESULT[0]["greetings"] == "Добрый день"

    # Проверяем что все функции были вызваны
    mock_greetings.assert_called_once()
    mock_cards.assert_called_once()
    mock_transactions.assert_called_once()
    mock_currency.assert_called_once()
    mock_stocks.assert_called_once()
    mock_search.assert_called_once_with("Константин Л.")
    mock_spending.assert_called_once_with("Каршеринг", date="27.12.2021")
