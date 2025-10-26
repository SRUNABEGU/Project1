from src.views import load_data

df = load_data()


def simple_search(search: str) -> dict:
    """осуществляет поиск по описанию или категории"""

    mask = df["Категория"].str.lower().str.contains(search.lower().strip(), na=False) | df[
        "Описание"
    ].str.lower().str.contains(search.lower().strip(), na=False)

    filtered_df = df[mask]

    return filtered_df.to_dict("records")
