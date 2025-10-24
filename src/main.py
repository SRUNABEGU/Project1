import json

from src.reports import spending_by_category
from src.services import simple_search
from src.views import RESULT, time_greetings, get_card_data, get_top_transactions, get_currency_rates, get_stock_prices


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
    print(json.dumps(simple_search("Константин Л."), indent=2, ensure_ascii=False))
    print(spending_by_category("Каршеринг", date="27.12.2021"))


if __name__ == "__main__":
    main()